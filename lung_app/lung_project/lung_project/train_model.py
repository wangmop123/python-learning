"""
Map widget using Leaflet rendered in QWebEngineView.
"""
import os
import json
from PyQt5.QtCore import pyqtSignal, QUrl, pyqtSlot
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QObject

from config import DEFAULT_LAT, DEFAULT_LON, DEFAULT_ZOOM
from config import COLOR_DRONE, COLOR_ROVER, COLOR_WAYPOINT, COLOR_PATH, COLOR_HOME


class MapBridge(QObject):
    """Bridge between JavaScript and Python."""

    waypoint_added = pyqtSignal(float, float)
    waypoint_moved = pyqtSignal(int, float, float)  # index, lat, lon
    waypoint_deleted = pyqtSignal(int)  # index
    home_position_set = pyqtSignal(float, float)  # lat, lon - for manual home setting
    map_clicked = pyqtSignal(float, float)

    @pyqtSlot(float, float)
    def on_map_click(self, lat, lon):
        self.map_clicked.emit(lat, lon)

    @pyqtSlot(float, float)
    def on_waypoint_add(self, lat, lon):
        self.waypoint_added.emit(lat, lon)

    @pyqtSlot(int, float, float)
    def on_waypoint_move(self, index, lat, lon):
        """Called when a waypoint is dragged to a new position."""
        self.waypoint_moved.emit(index, lat, lon)

    @pyqtSlot(int)
    def on_waypoint_delete(self, index):
        """Called when a waypoint is right-clicked for deletion."""
        self.waypoint_deleted.emit(index)

    @pyqtSlot(float, float)
    def on_home_set(self, lat, lon):
        """Called when home marker is moved."""
        self.home_position_set.emit(lat, lon)


class MapWidget(QWebEngineView):
    """Map display widget using Leaflet.js."""

    waypoint_added = pyqtSignal(float, float)
    waypoint_moved = pyqtSignal(int, float, float)  # index, lat, lon
    waypoint_deleted = pyqtSignal(int)  # index
    home_position_set = pyqtSignal(float, float)  # lat, lon
    map_clicked = pyqtSignal(float, float)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.bridge = MapBridge()
        self.bridge.waypoint_added.connect(self.waypoint_added)
        self.bridge.waypoint_moved.connect(self.waypoint_moved)
        self.bridge.waypoint_deleted.connect(self.waypoint_deleted)
        self.bridge.home_position_set.connect(self.home_position_set)
        self.bridge.map_clicked.connect(self.map_clicked)

        self.channel = QWebChannel()
        self.channel.registerObject("bridge", self.bridge)
        self.page().setWebChannel(self.channel)

        self._load_map()

    def _load_map(self):
        web_dir = os.path.join(os.path.dirname(__file__), "web")
        
        with open(os.path.join(web_dir, "map.css"), "r", encoding="utf-8") as f:
            css = f.read()
        with open(os.path.join(web_dir, "map.js"), "r", encoding="utf-8") as f:
            js = f.read()
        with open(os.path.join(web_dir, "map.html"), "r", encoding="utf-8") as f:
            html = f.read()

        # Inject constants into CSS
        css = css.replace("__COLOR_WAYPOINT__", COLOR_WAYPOINT)
        css = css.replace("__COLOR_HOME__", COLOR_HOME)

        # Inject constants into JS
        js = js.replace('"__DEFAULT_LAT__"', str(DEFAULT_LAT))
        js = js.replace('"__DEFAULT_LON__"', str(DEFAULT_LON))
        js = js.replace('"__DEFAULT_ZOOM__"', str(DEFAULT_ZOOM))
        js = js.replace("__COLOR_DRONE__", COLOR_DRONE)
        js = js.replace("__COLOR_ROVER__", COLOR_ROVER)
        js = js.replace("__COLOR_PATH__", COLOR_PATH)

        # Combine into HTML
        html = html.replace("<!-- INJECT_CSS -->", f"<style>\n{css}\n</style>")
        html = html.replace("<!-- INJECT_JS -->", f"<script>\n{js}\n</script>")

        self.setHtml(html)

    def update_vehicle(self, state):
        if not state.has_position():
            return

        label = (f"{state.name} | {state.mode} | "
                 f"Alt: {state.relative_alt:.1f}m | "
                 f"Spd: {state.groundspeed:.1f}m/s")

        js = (f"updateVehicle('{state.vehicle_type}', "
              f"{state.lat}, {state.lon}, {state.heading}, "
              f"'{label}');")
        self.page().runJavaScript(js)

    def update_trail(self, state):
        if len(state.trail) < 2:
            return

        points = state.trail[-200:]
        points_json = json.dumps(points)
        js = f"updateTrail('{state.vehicle_type}', '{points_json}');"
        self.page().runJavaScript(js)

    def update_home(self, lat, lon):
        """Update vehicle's home position (from telemetry)."""
        js = f"updateHome({lat}, {lon});"
        self.page().runJavaScript(js)

    def set_waypoints(self, waypoints):
        wp_data = [wp.to_dict() for wp in waypoints]
        wp_json = json.dumps(wp_data)
        js = f"setWaypoints('{wp_json}');"
        self.page().runJavaScript(js)

    def clear_waypoints(self):
        self.page().runJavaScript("clearWaypoints();")

    def center_on(self, lat, lon, zoom=None):
        if zoom:
            self.page().runJavaScript(f"centerMap({lat}, {lon}, {zoom});")
        else:
            self.page().runJavaScript(f"centerMap({lat}, {lon});")

    def set_adding_waypoints(self, enabled):
        js = f"setAddingWaypoints({'true' if enabled else 'false'});"
        self.page().runJavaScript(js)

    def set_waypoints_editable(self, enabled):
        """Enable or disable waypoint dragging."""
        js = f"setWaypointsEditable({'true' if enabled else 'false'});"
        self.page().runJavaScript(js)

    def fit_waypoints(self):
        """Zoom map to fit all waypoints."""
        self.page().runJavaScript("fitWaypoints();")