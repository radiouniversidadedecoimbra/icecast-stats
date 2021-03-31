function plot_map(countries, listeners, div) {

    var data = [{
            type: 'choropleth',
            locationmode: 'country names',
            locations: countries,
            z: listeners,
            text: countries,
            autocolorscale: true
        }];

    var layout = {
      title: 'Listeners',
      geo: {
          projection: {
              type: 'equirectangular'
          }
      }
    };

    var config = {responsive: true, showLink: false}

    Plotly.newPlot(div, data, layout, config);
}