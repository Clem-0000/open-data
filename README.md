# Satellite Tracker App

This project is a satellite tracker application that visualizes satellite orbits using **Cesium** and **Svelte**.

## Getting Started

### Prerequisites

Make sure you have the following installed:
- Node.js (v14 or higher)
- npm (v6 or higher)

### Installation

1. Clone the repository:
    ```sh
    https://github.com/Clem-0000/open-data.git
    ```

2. Install the dependencies:
    ```sh
    npm install
    ```

### Running the Application

To start the development server, run:
```sh
npm run dev
```

This will start the application at `http://localhost:5173`.

### Building for Production

To build the application for production, run:
```sh
npm run build
```

The production-ready files will be in the `dist` directory.

### Previewing the Production Build

To preview the production build, run:
```sh
npm run preview
```

## Data Sources

The satellite data is fetched from [N2YO](https://www.n2yo.com/). The data includes:
- Satellite TLE (Two-Line Element) data
- Satellite information by country

## Credits

- **Clément B.** - Developer
- **Arthur Z.** - Developer

## License

This project is licensed under the MIT License.