// dashboard/static/js/geographical_report.js

document.addEventListener('DOMContentLoaded', function() {
    // Fetch the country economic data from the JSON script tag
    const countryEconomicDataScript = document.getElementById('country-economic-data');
    if (!countryEconomicDataScript) {
        console.error('Country economic data script tag not found!');
        return;
    }

    let countryEconomicData;
    try {
        countryEconomicData = JSON.parse(countryEconomicDataScript.textContent);
        console.log('Country Economic Data:', countryEconomicData);
    } catch (error) {
        console.error('Error parsing country economic data:', error);
        return;
    }

    // Create a map from country name (lowercase) to data for quick lookup
    const countryDataMap = {};
    countryEconomicData.forEach(item => {
        if (item.name) {
            countryDataMap[item.name.toLowerCase()] = item;
        }
    });

    const width = window.innerWidth;
    const height = window.innerHeight;

    const svg = d3.select("#map-container")
        .append("svg")
        .attr("width", width)
        .attr("height", height);

    const projection = d3.geoNaturalEarth1()
        .scale(width / 2 / Math.PI)
        .translate([width / 2, height / 2]);

    const path = d3.geoPath().projection(projection);

    // Load world map data
    d3.json("https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json").then(function(world) {
        const countries = topojson.feature(world, world.objects.countries);

        svg.selectAll("path")
            .data(countries.features)
            .enter().append("path")
            .attr("d", path)
            .attr("class", "country")
            .on("click", showCountryInfo);
    }).catch(function(error){
        console.error('Error loading world map data:', error);
    });

    /**
     * Event handler for clicking on a country.
     * Displays macroeconomic information in the info panel.
     * If a PDF report is available, provides a download link.
     *
     * @param {Event} event - The click event.
     * @param {Object} d - The data object for the clicked country.
     */
    function showCountryInfo(event, d) {
        const countryName = d.properties.name.toLowerCase();
        const data = countryDataMap[countryName];

        if (data) {
            let reportLink = '';
            if (data.report_url) {
                reportLink = `<div class="info-item"><span class="info-label">گزارش کامل:</span> <a href="${data.report_url}" target="_blank">دانلود PDF</a></div>`;
            }

            const infoHTML = `
                <div class="info-item"><span class="info-label">کشور:</span> ${data.name}</div>
                <div class="info-item"><span class="info-label">جمعیت:</span> ${Number(data.population).toLocaleString()}</div>
                <div class="info-item"><span class="info-label">تولید ناخالص داخلی:</span> ${Number(data.gdp).toLocaleString()} دلار</div>
                <div class="info-item"><span class="info-label">تولید ناخالص داخلی سالانه:</span> ${Number(data.annual_gdp).toLocaleString()} دلار</div>
                <div class="info-item"><span class="info-label">امید به زندگی:</span> ${Number(data.life_expectancy).toFixed(2)} سال</div>
                ${reportLink}
            `;

            document.getElementById("country-info").innerHTML = infoHTML;
        } else {
            document.getElementById("country-info").innerHTML = `<p>اطلاعات برای این کشور موجود نیست.</p>`;
        }
    }

    // Responsive design: Adjust the map when the window is resized
    window.addEventListener('resize', function() {
        const newWidth = window.innerWidth;
        const newHeight = window.innerHeight;

        svg.attr("width", newWidth).attr("height", newHeight);
        projection.scale(newWidth / 2 / Math.PI).translate([newWidth / 2, newHeight / 2]);

        svg.selectAll("path").attr("d", path);
    });
});
