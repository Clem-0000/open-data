<script>
  import { onMount } from "svelte";
  import { Viewer, Ion, CzmlDataSource } from "cesium";
  import * as satellite from "satellite.js";

  async function getSatelliteInfo(norad_id) {
    const response = await fetch(
      `/api/rest/v1/satellite/tle/${norad_id}&apiKey=U9J3VY-5D8CUZ-7GNUDL-5CR1`
    );
    const data = await response.json();
    console.log(data);
    return data;
  }

  async function getAllSatInfo() {
    const response = await fetch("/french_satellites_shorten.json");
    const data = await response.json();
    console.log("json satellites", data);

    // Extraire les ID des satellites
    const satelliteIds = data.satellites.map((satellite) => satellite.norad_id);
    console.log("Satellite IDs:", satelliteIds);

    // Utiliser les ID extraits
    const satelliteInfo = [];
    for (let id of satelliteIds) {
      satelliteInfo.push(await getSatelliteInfo(id));
    }
    console.log("Satellite Info:", satelliteInfo);
    satelliteInfo.forEach((satelliteInfo) => {
      convertTLEtoCZML(satelliteInfo.tle);
    });
  }

  function convertTLEtoCZML(tle) {
    const tleLines = tle.split("\n");
    const tleLine1 = tleLines[0];
    const tleLine2 = tleLines[1];
    const satrec = satellite.twoline2satrec(tleLine1, tleLine2);

    // Generate positions for the next 24 hours
    const startTime = new Date();
    const endTime = new Date(startTime.getTime() + 24 * 60 * 60 * 1000);
    const positions = [];
    const step = 60 * 1000; // 1 minute step

    for (
      let time = startTime;
      time <= endTime;
      time = new Date(time.getTime() + step)
    ) {
      const positionAndVelocity = satellite.propagate(satrec, time);
      const gmst = satellite.gstime(time);
      if (typeof positionAndVelocity.position !== "boolean") {
        const position = satellite.eciToEcf(positionAndVelocity.position, gmst);
        positions.push(time.toISOString());
        positions.push(position.x * 1000); // Convert to meters
        positions.push(position.y * 1000);
        positions.push(position.z * 1000);
      } else {
        console.error("Invalid position data");
      }
    }

    // Create CZML document
    const czml = [
      {
        id: "document",
        name: "CZML Satellite Orbit",
        version: "1.0",
      },
      {
        id: satrec.satnum,
        name: `Satellite ${satrec.satnum}`,
        availability: `${startTime.toISOString()}/${endTime.toISOString()}`,
        billboard: {
          eyeOffset: {
            cartesian: [0, 0, 0],
          },
          horizontalOrigin: "CENTER",
          image:
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAADJSURBVDhPnZHRDcMgEEMZjVEYpaNklIzSEfLfD4qNnXAJSFWfhO7w2Zc0Tf9QG2rXrEzSUeZLOGm47WoH95x3Hl3jEgilvDgsOQUTqsNl68ezEwn1vae6lceSEEYvvWNT/Rxc4CXQNGadho1NXoJ+9iaqc2xi2xbt23PJCDIB6TQjOC6Bho/sDy3fBQT8PrVhibU7yBFcEPaRxOoeTwbwByCOYf9VGp1BYI1BA+EeHhmfzKbBoJEQwn1yzUZtyspIQUha85MpkNIXB7GizqDEECsAAAAASUVORK5CYII=",
          pixelOffset: {
            cartesian2: [0, 0],
          },
          scale: 1.5,
          show: true,
          verticalOrigin: "CENTER",
        },
        position: {
          epoch: startTime.toISOString(),
          cartesian: positions,
        },
        path: {
          material: {
            solidColor: {
              color: {
                rgba: [255, 0, 0, 255],
              },
            },
          },
          width: 1,
          leadTime: 0,
          trailTime: 60 * 60 * 24,
          resolution: 120,
        },
      },
    ];

    // Ajouter le CZML à Cesium
    const czmlDataSource = new CzmlDataSource();
    czmlDataSource
      .load(czml)
      .then(() => {
        viewer.dataSources.add(czmlDataSource);
        console.log(`Satellite ${satrec.satnum} ajouté à la carte.`);
      })
      .catch((error) => {
        console.error("Erreur lors du chargement du CZML :", error);
      });
  }

  let viewer;

  // TODO : Check warning in the console and correct them (maybe used bing maps for correcting http error without S)
  // Initialize Cesium Viewer
  onMount(() => {
    // TODO : Hide in ENV the access token
    Ion.defaultAccessToken =
      "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI4ODRlMDAyOC1jMTk1LTQ0YzMtYWI4Yy1mMGRhOTVlNTRjOGUiLCJpZCI6MjQ4MDcxLCJpYXQiOjE3Mjg5MTkyOTd9.E1s0Ltamk-LNAm3ZEYLBflltEbevlPzNzhhgXpJCj3U";

    // Initialize the Cesium Viewer
    viewer = new Viewer("cesiumContainer", {
      shouldAnimate: true,
    });
  });

  getAllSatInfo();
</script>

<main>
  <div id="cesiumContainer"></div>
</main>

<style>
  #cesiumContainer {
    width: 100%;
    height: 100vh;
    margin: 0;
    padding: 0;
    overflow: hidden;
  }

  main {
    margin: 0;
    padding: 0;
    overflow: hidden;
  }
</style>
