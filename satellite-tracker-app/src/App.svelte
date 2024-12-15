<script>
  import { onMount } from "svelte";
  import {
    Viewer,
    Ion,
    CzmlDataSource,
    ClockStep,
    ClockRange,
    JulianDate,
  } from "cesium";
  import * as satellite from "satellite.js";

  const SATELLITES_DATA_URL = "/satellites_data.json";
  const TLE_DATA_URL = "/tle_data.json";

  let countries = [];
  let selectedCountry = "";
  let satelliteData = {};
  let tleData = {};
  let viewer;
  let czmlDataSources = [];

  async function getUserCountry() {
  try {
    const response = await fetch('https://ipapi.co/json/');
    const data = await response.json();
    console.log('User country:', data.country_name);
    return data.country_name;
  } catch (error) {
    console.error('Error fetching user country:', error);
    return null;
  }
}

  // Fetch satellite information for a specific NORAD ID
  async function getSatelliteInfo(norad_id) {
    try {
      const response = await fetch(
        `/api/rest/v1/satellite/tle/${norad_id}&apiKey=U9J3VY-5D8CUZ-7GNUDL-5CR1`
      );
      const data = await response.json();

      if (!data || !data.tle || !data.tle.includes("\n")) {
        return null;
      }

      return data;
    } catch (error) {
      console.error(
        `Error fetching satellite info for NORAD ID ${norad_id}:`,
        error
      );
      return null;
    }
  }

  // Fetch all satellite data
  async function fetchSatelliteData() {
    const response = await fetch(SATELLITES_DATA_URL);
    const data = await response.json();
    satelliteData = data;

    countries = Object.keys(data);
  }

  // Fetch all TLE data
  async function fetchTLEData() {
    const response = await fetch(TLE_DATA_URL);
    const data = await response.json();

    tleData = data;
  }

  function clearSatellites() {
    czmlDataSources.forEach((dataSource) => {
      viewer.dataSources.remove(dataSource, true);
    });
    czmlDataSources = [];
  }

  async function loadSatellitesForCountry() {
    if (!selectedCountry || !satelliteData[selectedCountry]) return;

    clearSatellites();

    const satelliteIds = satelliteData[selectedCountry];
    for (let id of satelliteIds) {
      const satInfo = await getSatelliteInfo(id);
      if (satInfo) {
        convertTLEtoCZML(satInfo.tle, satInfo.info.satname);
      } else {
        const satInfo = tleData[id];
        if (satInfo) {
          if (!satInfo.tle || !satInfo.tle.includes("\n")) {
            console.warn(
              `Skipping satellite with ID ${id} due to missing TLE data.`
            );
            continue;
          }
          convertTLEtoCZML(satInfo.tle, satInfo.satname);
        } else {
          console.warn(
            `Skipping satellite with ID ${id} due to missing TLE data.`
          );
        }
      }
    }
  }

  // Convert TLE data to CZML and load into Cesium
  function convertTLEtoCZML(tle, satInfo) {
    const tleLines = tle.split("\n");
    const tleLine1 = tleLines[0];
    const tleLine2 = tleLines[1];
    const satrec = satellite.twoline2satrec(tleLine1, tleLine2);

    const startTime = new Date();
    const endTime = new Date(startTime.getTime() + 24 * 60 * 60 * 1000);
    const positions = [];
    const step = 60 * 1000;

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
        positions.push(position.x * 1000);
        positions.push(position.y * 1000);
        positions.push(position.z * 1000);
      }
    }

    const czml = [
      {
        id: "document",
        name: "CZML Satellite Orbit",
        version: "1.0",
      },
      {
        id: satrec.satnum,
        name: `${satInfo}`,
        availability: `${startTime.toISOString()}/${endTime.toISOString()}`,
        billboard: {
          eyeOffset: { cartesian: [0, 0, 0] },
          horizontalOrigin: "CENTER",
          image:
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAADJSURBVDhPnZHRDcMgEEMZjVEYpaNklIzSEfLfD4qNnXAJSFWfhO7w2Zc0Tf9QG2rXrEzSUeZLOGm47WoH95x3Hl3jEgilvDgsOQUTqsNl68ezEwn1vae6lceSEEYvvWNT/Rxc4CXQNGadho1NXoJ+9iaqc2xi2xbt23PJCDIB6TQjOC6Bho/sDy3fBQT8PrVhibU7yBFcEPaRxOoeTwbwByCOYf9VGp1BYI1BA+EeHhmfzKbBoJEQwn1yzUZtyspIQUha85MpkNIXB7GizqDEECsAAAAASUVORK5CYII=",
          pixelOffset: { cartesian2: [0, 0] },
          scale: 1.5,
          show: true,
          verticalOrigin: "CENTER",
        },
        position: {
          epoch: startTime.toISOString(),
          cartesian: positions,
        },
        /*path: {
          material: {
            solidColor: {
              color: { rgba: [255, 0, 0, 255] },
            },
          },
          width: 1,
          leadTime: 0,
          trailTime: 60 * 60 * 24,
          resolution: 120,
        },*/
      },
    ];

    const czmlDataSource = new CzmlDataSource();
    czmlDataSource
      .load(czml)
      .then(() => {
        viewer.dataSources.add(czmlDataSource);
        czmlDataSources.push(czmlDataSource);
      })
      .catch((error) => console.error("Error loading CZML:", error));
  }

  // Initialize Cesium viewer
  onMount(async () => {
    Ion.defaultAccessToken =
      "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI4ODRlMDAyOC1jMTk1LTQ0YzMtYWI4Yy1mMGRhOTVlNTRjOGUiLCJpZCI6MjQ4MDcxLCJpYXQiOjE3Mjg5MTkyOTd9.E1s0Ltamk-LNAm3ZEYLBflltEbevlPzNzhhgXpJCj3U";

    viewer = new Viewer("cesiumContainer", {
      shouldAnimate: true,
      automaticallyTrackDataSourceClocks: false,
    });

    const clock = viewer.clock;
    clock.clockStep = ClockStep.SYSTEM_CLOCK;
    clock.clockRange = ClockRange.UNBOUNDED;
    clock.currentTime = JulianDate.now();
    clock.multiplier = 1;

    await fetchSatelliteData();
    await fetchTLEData();

    selectedCountry = countries[0]; // We want France as default country (Vive la baguette)
    await loadSatellitesForCountry();
  });

  $: if (selectedCountry) loadSatellitesForCountry();
</script>

<main>
  <div class="containerSelector">
    <select id="country-selector" bind:value={selectedCountry}>
      {#each countries as country}
        <option value={country}
          >{country} ({satelliteData[country].length})</option
        >
      {/each}
    </select>
  </div>
  <div class="informationPanel">
    <h1>Information Panel</h1>
    <p>Dataset coming from : https://www.n2yo.com/</p>
    <p>Author : Clément B. and Arthur Z.</p>
  </div>
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
    position: relative;
  }

  .containerSelector {
    position: absolute;
    top: 10px;
    left: 10px;
    z-index: 10;
    background-color: rgba(0, 0, 0, 0.5);
    padding: 5px;
    border-radius: 5px;
  }

  .informationPanel {
    position: absolute;
    top: 50px;
    right: 10px;
    z-index: 10;
    color: #fff;
    background-color: rgba(0, 0, 0, 0.5);
    padding: 5px;
    border-radius: 5px;
  }

  select {
    padding: 5px;
    font-size: 1rem;
    color: #fff;
    background-color: #2a2a2a;
    border: 1px solid #555;
    border-radius: 3px;
  }

  select:focus {
    outline: none;
    border-color: #00aaff;
  }
</style>
