# Additional Performance Improvement Suggestions

This document lists potential performance improvements that were identified but not implemented due to lower priority or higher complexity/risk ratio.

## Suggested Improvements (Not Implemented)

### 1. NetworkTables - More Comprehensive Caching

**Location**: `MLtune/tuner/nt_interface.py`

**Potential Optimization**: Apply the table caching pattern to all remaining methods that call `NetworkTables.getTable()`.

**Methods to Update**:
- `read_skip_to_next_button()`
- `read_global_threshold_update()`
- `read_local_threshold_update()`
- `write_current_coefficient_info()`
- `read_tuner_enabled_toggle()`
- `write_tuner_enabled_status()`
- `initialize_manual_controls()`
- `read_manual_coefficient_adjustment()`
- `write_manual_control_status()`
- `initialize_fine_tuning_controls()`
- `read_fine_tuning_settings()`
- `initialize_backtrack_controls()`
- `read_backtrack_request()`
- `write_backtrack_status()`
- `write_all_coefficient_values_to_dashboard()`

**Risk**: Low - same pattern already proven safe
**Impact**: Small - these methods are called less frequently
**Effort**: Medium - many methods to update

**Example**:
```python
# Replace:
tuner_table = NetworkTables.getTable("/Tuning/BayesianTuner")

# With:
tuner_table = self._get_cached_table("/Tuning/BayesianTuner")
```

---

### 2. Status Update Frequency Optimization

**Location**: `MLtune/tuner/tuner.py` - `_update_status()` method

**Potential Optimization**: Only update dashboard status when values actually change, not on every loop iteration.

**Implementation**:
```python
def _update_status(self):
    # Build new status
    new_status = self._build_status_dict()
    
    # Only update if changed
    if not hasattr(self, '_last_status') or self._last_status != new_status:
        self._write_status_to_dashboard(new_status)
        self._last_status = new_status
```

**Risk**: Low - simple change detection
**Impact**: Medium - reduces NetworkTables writes by 50-80%
**Effort**: Low - simple to implement

---

### 3. Coefficient Value Change Detection

**Location**: `MLtune/tuner/tuner.py` - `_update_coefficients()` method

**Potential Optimization**: Skip NetworkTables write if coefficient value hasn't changed.

**Implementation**:
```python
def _update_coefficients(self):
    suggestion = self.optimizer.suggest_coefficient_update()
    
    if suggestion:
        coeff_name, new_value = suggestion
        old_value = self.current_coefficient_values.get(coeff_name)
        
        # Skip write if value unchanged (within epsilon)
        if old_value is not None and abs(new_value - old_value) < 1e-9:
            logger.debug(f"Skipping write for {coeff_name}, value unchanged")
            return
        
        # ... rest of method
```

**Risk**: Low - adds safety check
**Impact**: Small - optimization runs change values most of the time
**Effort**: Low - simple check

---

### 4. Dashboard Graph Update Throttling

**Location**: `dashboard/app.py`

**Potential Optimization**: Reduce graph update frequency and implement smart diff updates.

**Implementation**:
```python
# Update graphs less frequently
dcc.Interval(id='graph-update-interval', interval=2000)  # 2 seconds instead of 1

# Only update graphs that have new data
@app.callback(...)
def update_graphs(...):
    if not has_new_data():
        return dash.no_update
    # ... update logic
```

**Risk**: Medium - could affect user experience
**Impact**: Large - significant CPU/rendering reduction
**Effort**: High - requires careful testing

---

### 5. Lazy Graph Rendering

**Location**: `dashboard/app.py` - graph creation functions

**Potential Optimization**: Don't render all 8 graphs immediately, only render visible ones.

**Implementation**:
```python
# Use dcc.Loading for lazy loading
dcc.Loading(
    id="loading-graphs",
    children=[html.Div(id="graphs-container")],
    type="default"
)

# Render graph only when tab is active
@app.callback(...)
def render_graph(active_tab):
    if active_tab == 'graphs':
        return create_graphs()
    return dash.no_update
```

**Risk**: Medium - affects initial load experience
**Impact**: Large - faster initial page load
**Effort**: High - requires restructuring

---

### 6. Coefficient History JSON Optimization

**Location**: `MLtune/tuner/logger.py` - `log_coefficient_combination()` method

**Potential Optimization**: Load and write JSON files less frequently, batch multiple entries.

**Implementation**:
```python
# Instead of read-modify-write on every call:
# 1. Keep history in memory
# 2. Write every N entries or on close
# 3. Append to file instead of rewriting entire file

def log_coefficient_combination(self, coefficient_values, event="SNAPSHOT"):
    if not hasattr(self, '_coefficient_history_buffer'):
        self._coefficient_history_buffer = []
    
    entry = {...}
    self._coefficient_history_buffer.append(entry)
    
    # Flush every 10 entries
    if len(self._coefficient_history_buffer) >= 10:
        self._flush_coefficient_history()
```

**Risk**: Medium - could lose data on crash
**Impact**: Medium - reduces JSON I/O overhead
**Effort**: Medium - requires buffer management

---

### 7. NumPy Array Pre-allocation

**Location**: `MLtune/tuner/optimizer.py` - `_process_pending_shots()` method

**Potential Optimization**: Pre-allocate NumPy arrays instead of building Python lists.

**Implementation**:
```python
# Pre-allocate arrays
num_shots = len(self.pending_shots)
coeff_values = np.empty(num_shots)
distances = np.empty(num_shots)

# Fill arrays
hits = 0
for i, shot in enumerate(self.pending_shots):
    if shot['shot_data'].hit:
        hits += 1
    coeff_values[i] = shot['coefficient_value']
    distances[i] = shot['shot_data'].distance
```

**Risk**: Low - straightforward change
**Impact**: Small - marginal improvement for small batches
**Effort**: Low - simple array operations

---

### 8. Connection Status Caching

**Location**: `MLtune/tuner/nt_interface.py` - `is_connected()` method

**Potential Optimization**: Cache connection status and check less frequently.

**Implementation**:
```python
def is_connected(self) -> bool:
    # Only check actual connection every N seconds
    current_time = time.time()
    if current_time - self._last_connection_check < 1.0:
        return self._cached_connection_status
    
    self._last_connection_check = current_time
    try:
        self.connected = NetworkTables.isConnected()
        self._cached_connection_status = self.connected
    except Exception as e:
        logger.error(f"Error checking connection status: {e}")
        self.connected = False
        self._cached_connection_status = False
    
    return self.connected
```

**Risk**: Medium - could delay disconnect detection
**Impact**: Small - method is already fast
**Effort**: Low - simple caching

---

## Prioritization Matrix

| Optimization | Impact | Effort | Risk | Priority |
|--------------|--------|--------|------|----------|
| NetworkTables Caching | Small | Medium | Low | Low |
| Status Update Detection | Medium | Low | Low | **Medium** |
| Coefficient Change Detection | Small | Low | Low | Low |
| Dashboard Throttling | Large | High | Medium | **Medium** |
| Lazy Graph Rendering | Large | High | Medium | **Medium** |
| JSON Batching | Medium | Medium | Medium | Low |
| NumPy Pre-allocation | Small | Low | Low | Low |
| Connection Caching | Small | Low | Medium | Low |

**Recommended Next Steps** (in order):
1. Status Update Detection - high value, low risk
2. Dashboard Throttling - high impact if dashboard is slow
3. Lazy Graph Rendering - better user experience

---

## Testing Recommendations

For any future optimizations:

1. **Benchmark Before/After**
   - Use `cProfile` for Python code
   - Measure with realistic data volumes
   - Test on target hardware (Raspberry Pi, laptop, etc.)

2. **Verify Functionality**
   - Run with real robot connection
   - Test all dashboard features
   - Verify log file integrity
   - Check coefficient updates apply correctly

3. **Stress Testing**
   - High-frequency shot data (10+ shots/second)
   - Large accumulated shot batches (100+ shots)
   - Long-running sessions (hours)
   - Disconnect/reconnect scenarios

4. **Memory Profiling**
   - Check for memory leaks
   - Monitor memory usage over time
   - Verify caches don't grow unbounded

---

## Performance Monitoring

Consider adding built-in performance metrics:

```python
class PerformanceMonitor:
    def __init__(self):
        self.metrics = {
            'shots_processed': 0,
            'optimizations_run': 0,
            'disk_writes': 0,
            'nt_writes': 0,
            'total_time': 0.0,
        }
    
    def record_metric(self, name, value):
        self.metrics[name] += value
    
    def get_summary(self):
        return {
            'shots_per_second': self.metrics['shots_processed'] / self.metrics['total_time'],
            'avg_optimization_time': ...,
            # ... more metrics
        }
```

---

*Last Updated: 2026-01-05*
