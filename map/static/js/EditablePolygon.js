(function (Gm) {
	/// @class An editable polygon.
	var EditablePolygon = Gm.EditablePolygon = function (options) {
		Gm.ObservablePolygon.call(this, options);

		this.dragPolyline = new Gm.Polyline({
			strokeColor: "yellow",
			strokeWeight: 1,

			clickable: false
		});

		this.markerImage = new Gm.MarkerImage(this.handleImage);
		this.markerImage.anchor = new Gm.Point(5, 5);
	};

	/// @extends ObservablePolygon
	EditablePolygon.prototype = new Gm.ObservablePolygon();

	EditablePolygon.prototype.setMap = function (map) {
		Gm.ObservablePolygon.prototype.setMap.apply(this, arguments);

		this.dragPolyline.setMap(map);
	};

	EditablePolygon.prototype.beginEdit = function () {
		if (!this.editing) {
			this.editing = true;

			this.focusedIndex = 0;
			this.focusedPoints = [];

			this.mapClickListener = Gm.event.addListener(this.map, "click", this.onMapClick.bind(this));
			this.innerClickListener = Gm.event.addListener(this, "click", this.onMapClick.bind(this));
			this.mapMouseMoveListener = Gm.event.addListener(this.map, "mousemove", this.onMapMouseMove.bind(this));
			this.innerMouseMoveListener = Gm.event.addListener(this, "mousemove", this.onMapMouseMove.bind(this));
			this.mapMouseOutListener = Gm.event.addListener(this.map, "mouseout", this.onMapMouseOut.bind(this));

			this.getPath().forEach(function (point) {
				point.marker.setVisible(true);
			});
		}
	};

	EditablePolygon.prototype.endEdit = function () {
		if (this.editing) {
			Gm.event.removeListener(this.mapClickListener);
			Gm.event.removeListener(this.innerClickListener);
			Gm.event.removeListener(this.mapMouseMoveListener);
			Gm.event.removeListener(this.innerMouseMoveListener);
			Gm.event.removeListener(this.mapMouseOutListener);

			this.editing = false;

			this.focusedIndex = null;

			this.getPath().forEach(function (point) {
				point.marker.setVisible(false);
			});
		}
	};

	/// @protected Creates a marker.
	EditablePolygon.prototype.createMarker = function (options) {
		var marker = new Gm.Marker({
			position: options.position,

			draggable: true,
			raiseOnDrag: false,
			flat: true,
			visible: this.editing,

			icon: this.markerImage,

			map: this.map
		});

		marker.point = options.position;

		marker.dragEndListener = Gm.event.addListener(marker, "dragend", this.onMarkerDragEnd.bind(this, marker));
		marker.dragStartListener = Gm.event.addListener(marker, "dragstart", this.onMarkerDragStart.bind(this));
		marker.mouseOverListener = Gm.event.addListener(marker, "mouseover", this.onMarkerMouseOver.bind(this));

		return marker;
	};

	/// @protected Destroys the marker.
	EditablePolygon.prototype.destroyMarker = function (marker) {
		marker.setMap(null);

		Gm.event.removeListener(marker.dragEndListener);
		Gm.event.removeListener(marker.dragStartListener);
		Gm.event.removeListener(marker.mouseOverListener);
	};

	/// @override Sets the path of the polygon.
	EditablePolygon.prototype.setPath = function (path) {
		Gm.ObservablePolygon.prototype.setPath.apply(this, arguments);

		// Add the existing points
		var path = this.getPath(), len = path.getLength(), 
			me = this;

		path.forEach(function (point, index) {
			// Add the marker for the point
			point.marker = this.createMarker({
				position: point
			});
		})
	};

	/// @protected @override
	EditablePolygon.prototype.onPathPointInserted = function (index) {
		Gm.ObservablePolygon.prototype.onPathPointInserted.apply(this, arguments);

		var path = this.getPath(), point = path.getAt(index);

		// Add the marker for the point
		point.marker = this.createMarker({
			position: point
		});
	};
    EditablePolygon.prototype.contains = function(point) {
        var j=0;
        var oddNodes = false;
        var x = point.lng();
        var y = point.lat();

        var paths = this.getPath();
        console.log(paths)
        for (var i=0; i < paths.getLength(); i++) {
            j++;
            if (j == paths.getLength()) {j = 0;}
                if (((paths.getAt(i).lat() < y) && (paths.getAt(j).lat() >= y)) || ((paths.getAt(j).lat() < y) && (paths.getAt(i).lat() >= y))) {
                    if ( paths.getAt(i).lng() + (y - paths.getAt(i).lat())
                    /  (paths.getAt(j).lat()-paths.getAt(i).lat())
                    *  (paths.getAt(j).lng() - paths.getAt(i).lng())<x ) {
                            oddNodes = !oddNodes
                    }
            }
        }
        return oddNodes;
    }
	/// @protected @override
	EditablePolygon.prototype.onPathPointRemoved = function (index, point) {
		Gm.ObservablePolygon.prototype.onPathPointRemoved.apply(this, arguments);

		this.destroyMarker(point.marker);
	};

	EditablePolygon.prototype.onMapMouseMove = function (e) {
		if (this.focusedIndex !== null) {
			var path = this.getPath(), len = path.getLength();

			if (len == 1) {
				var points = [ path.getAt(this.focusedIndex), e.latLng ];

				this.dragPolyline.setPath(points);
			}
			else if (len > 1 && this.focusedPoints.length > 0) {
				var points = [ this.focusedPoints[0], e.latLng, this.focusedPoints[1] ];

				this.dragPolyline.setPath(points);
			}
		}
	};

	EditablePolygon.prototype.onMapMouseOut = function (e) {
		if (this.getPath().getLength() > 2) {
			this.focusedIndex = null;
			this.dragPolyline.setPath([]);
		}
	};

	EditablePolygon.prototype.onMarkerMouseOver = function () {
		if (this.getPath().getLength() > 2) {
			this.focusedIndex = null;
			this.dragPolyline.setPath([]);
		}
	};

	EditablePolygon.prototype.onMarkerDragStart = function () {
		if (this.getPath().getLength() > 2) {
			this.focusedIndex = null;
			this.dragPolyline.setPath([]);
		}
	};

	EditablePolygon.prototype.onMarkerDragEnd = function (marker, e) {
		this.getPath().setAt(marker.point.index, e.latLng);
		
		marker.point = e.latLng;
	};

	EditablePolygon.prototype.onMapClick = function (e) {
		if (this.focusedIndex !== null) {
			this.getPath().insertAt(this.focusedIndex, e.latLng);

		}
	};

	EditablePolygon.prototype.onMarginFocus = function (index, margin) {
		this.focusedIndex = index + 1;
		this.focusedPoints = margin.getPath().getArray();

		Gm.ObservablePolygon.prototype.onMarginFocus.apply(this, arguments);
	};

	return EditablePolygon;
})(google.maps);