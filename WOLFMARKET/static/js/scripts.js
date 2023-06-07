/*!
* Start Bootstrap - Landing Page v6.0.5 (https://startbootstrap.com/theme/landing-page)
* Copyright 2013-2022 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-landing-page/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project
function updateChart() {
    // Obtener el ticker seleccionado
    var ticker = document.getElementById("ticker").value;
    
    // Realizar la consulta a CCXT para obtener los datos del ticker
    fetch(`/chart_data/${ticker}`)
      .then((response) => response.json())
      .then((data) => {
        // Convertir los datos a un formato compatible con Lightweight Charts
        var chartData = data.map((row) => {
          return {
            time: row[0],
            open: row[1],
            high: row[2],
            low: row[3],
            close: row[4],
            volume: row[5]
          };
        });
        
        // Actualizar los datos del gráfico
        chart.applyOptions({ timeScale: { rightOffset: 12 } }); // ajustar la escala de tiempo
        chart.update(chartData); // actualizar los datos del gráfico
      })
      .catch((error) => {
        console.error("Error al obtener los datos del gráfico:", error);
      });
  }
  