<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <!-- Include the CesiumJS JavaScript and CSS files -->
    <script src="https://cesium.com/downloads/cesiumjs/releases/1.122/Build/Cesium/Cesium.js"></script>
    <link href="https://cesium.com/downloads/cesiumjs/releases/1.122/Build/Cesium/Widgets/widgets.css" rel="stylesheet">
</head>

<body>
    <div id="cesiumContainer"></div>
    <script type="module">
        // Your access token can be found at: https://ion.cesium.com/tokens.
        // Replace `your_access_token` with your Cesium ion access token.

        Cesium.Ion.defaultAccessToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI4ODRlMDAyOC1jMTk1LTQ0YzMtYWI4Yy1mMGRhOTVlNTRjOGUiLCJpZCI6MjQ4MDcxLCJpYXQiOjE3Mjg5MTkyOTd9.E1s0Ltamk-LNAm3ZEYLBflltEbevlPzNzhhgXpJCj3U';

        // Initialize the Cesium Viewer in the HTML element with the `cesiumContainer` ID.
        const viewer = new Cesium.Viewer('cesiumContainer', {
            terrain: Cesium.Terrain.fromWorldTerrain(),
        });
    </script>
    </div>
</body>

</html>