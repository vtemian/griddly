function CheckinOverlay(text, point, map) {
  this.map_ = map;
  this.text_ = text;
  this.point_ = point;
  this.setMap(map);
}

CheckinOverlay.prototype = new google.maps.OverlayView();

CheckinOverlay.prototype.onAdd = function() {
    var div = document.createElement('DIV');
    div.style.border = "none";
    div.style.borderWidth = "0px";
    div.style.position = "absolute";
    div.innerHTML = this.text_;
    var panes = this.getPanes();
    this.div_ = div;
    panes.overlayLayer.appendChild(this.div_);
}

CheckinOverlay.prototype.draw = function() {

    var overlayProjection = this.getProjection();
    
    var point = overlayProjection.fromLatLngToDivPixel(this.point_);

    var div = this.div_;

    div.style.left = point.x + 'px';
    div.style.top = point.y + 'px';
}