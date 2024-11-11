function updateSatellite() {
    let fetched_data = [];

    fetch('french_satellites.json')
    .then(response => response.json())
    .then(data => {
        console.log("Update Time " + Date());

        const fetchPromises = data['satellites'].map(satellite => {
            return fetch('satellite.php?norad_id=' + satellite['norad_id'])	
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.json();
            })
            .then(data => {
                fetched_data.push(data);
                console.log(data);
                return data;
            })
            .catch(error => {
                console.log(`Error: ${error.message}`);
            });
        });

        return Promise.all(fetchPromises);
    })
    .then(() => {
        // Here you can do something with the fetched_data array
        console.log("All data fetched:", fetched_data);
        // Instead of writing to a file, you could update the UI or do other operations
    })
    .catch(error => console.error('Error loading JSON:', error));
}

// Call updateSatellite immediately
updateSatellite();

// Then set interval to call it every 60 minutes
setInterval(updateSatellite, 60 * 60000);
