// Dark mode support for Plotly graphs
(function() {
    // Function to get CSS variable value
    function getCSSVariable(name) {
        return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
    }
    
    // Function to update all Plotly graphs for current theme
    function updatePlotlyGraphs() {
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        
        // Get theme colors
        const bgColor = getCSSVariable('--bg-primary');
        const paperColor = getCSSVariable('--bg-secondary');
        const gridColor = getCSSVariable('--border-default');
        const textColor = getCSSVariable('--text-primary');
        
        // Find all plotly graphs
        const graphs = document.querySelectorAll('.js-plotly-plot');
        
        graphs.forEach(graph => {
            if (graph && graph.layout) {
                const update = {
                    'paper_bgcolor': paperColor,
                    'plot_bgcolor': bgColor,
                    'font.color': textColor,
                    'xaxis.gridcolor': gridColor,
                    'yaxis.gridcolor': gridColor,
                    'xaxis.color': textColor,
                    'yaxis.color': textColor
                };
                
                // Update the graph
                try {
                    Plotly.relayout(graph, update);
                } catch (e) {
                    console.log('Could not update graph:', e);
                }
            }
        });
    }
    
    // Update graphs when page loads
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(updatePlotlyGraphs, 500);
        });
    } else {
        setTimeout(updatePlotlyGraphs, 500);
    }
    
    // Watch for theme changes
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.attributeName === 'data-theme') {
                setTimeout(updatePlotlyGraphs, 100);
            }
        });
    });
    
    observer.observe(document.documentElement, {
        attributes: true,
        attributeFilter: ['data-theme']
    });
    
    // Also listen for Dash callback completions
    if (window.dash_clientside) {
        window.dash_clientside.plotly_update = {
            update_on_theme: function() {
                setTimeout(updatePlotlyGraphs, 100);
                return window.dash_clientside.no_update;
            }
        };
    }
})();
