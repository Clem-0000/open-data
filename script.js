import fs from 'fs';

function updateSatellite() {
    let fetched_data = []

    fetch('french_satellites.json')
    .then(response => response.json()) // Parse JSON response
    .then(data => {
        console.log("Update Time " + Date());

        data['satellites'].forEach(satellite => {
            fetch('satellite.php?norad_id=' + satellite['norad_id'])	
            .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.text();
            })
            .then(data => {
                fetched_data.push(data);
                console.log(data);
            })
            .catch(error => {
                console.log(`Error: ${error.message}`);
            });
        });

        const save = JSON.stringify(fetched_data);

        fs.writeFile("data.json", save, (error) => {
            if (error) {
                console.error(error);
                throw error;
            }
        });
    })
    .catch(error => console.error('Error loading JSON:', error));
};

setInterval(function () {
    updateSatellite();
}, 60 * 60000); //every 60 minutes