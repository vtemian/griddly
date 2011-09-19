(function (Gm) {
	/// @class A polygon with observable individual margins.
	var ObservablePolygon = Gm.ObservablePolygon = function (options) {
		Gm.Polygon.call(this, options);

		this.highlightMargins = options ? options.highlightMargins : false;

		// {Gm.MVCArray} The list of polygon margins.
		this.margins = new Gm.MVCArray();
		this.bindToPath(this.getPath());
	};

	// @extends Gm.Polygon
	ObservablePolygon.prototype = new Gm.Polygon();

	/// @override Sets the path of the polygon.
	ObservablePolygon.prototype.setPath = function (path) {
		this.unbindFromPath();
        
		Gm.Polygon.prototype.setPath.apply(this, arguments);

		// Add the existing points
		var path = this.getPath(), len = path.getLength(), 
			me = this;

		path.forEach(function (point, index) {
			point.index = index;

			var margin = me.createMargin({
				path: [ point, path.getAt(index == len - 1 ? 0 : index + 1) ],

				index: index
			});

			me.margins.push(margin);
		});

		this.bindToPath(path);
	};

	/// @protected Unbinds from the path events.
	ObservablePolygon.prototype.unbindFromPath = function () {
		if (this.boundTopath) {
			Gm.event.removeListener(this.pathPointInsertedListener);
			Gm.event.removeListener(this.pathPointRemovedListener);
			Gm.event.removeListener(this.pathPointSetListener);

			this.boundToPath = false;
		}
	};

	/// @protected Binds to the path events.
	ObservablePolygon.prototype.bindToPath = function (path) {
		this.pathPointInsertedListener = Gm.event.addListener(path, "insert_at", this.onPathPointInserted.bind(this));
		this.pathPointRemovedListener = Gm.event.addListener(path, "remove_at", this.onPathPointRemoved.bind(this));
		this.pathPointSetListener = Gm.event.addListener(path, "set_at", this.onPathPointSet.bind(this));

		this.boundToPath = true;
	};

	/// @protected Creates a new margin.
	ObservablePolygon.prototype.createMargin = function (options) {
		var margin = new google.maps.Polyline({
			strokeOpacity: this.highlightMargins === true ? 0.5 : 0,
			strokeColor: "green",
			strokeWeight: 8,

			path: options.path,

			map: this.map
		});

		margin.index = options.index;

		margin.mouseMoveListener = Gm.event.addListener(margin, "mousemove", this.onMarginMouseMove.bind(this, margin));

		return margin;
	};

	/// @protected Destroys the margin.
	ObservablePolygon.prototype.destroyMargin = function (margin) {
		margin.setMap(null);

		Gm.event.removeListener(margin.mouseMoveListener);
	};

	/// @protected Handles when a point is inserted in the path.
	ObservablePolygon.prototype.onPathPointInserted = function (index) {
		var path = this.getPath(), len = path.getLength(),
			newPoint = path.getAt(index);

		if (len == 2) {
			// Ass the first margin
			var lastPoint = path.getAt(index == 0 ? 1 : 0);

			var margin = this.createMargin({
				path: [ lastPoint, newPoint ],

				index: 0
			});

			this.margins.push(margin);
		}
		else if (len > 2) {
			if (index == 0) {
				var indexRight = 1, indexLeft = len - 1,
					pointRight = path.getAt(indexRight), pointLeft = path.getAt(indexLeft);

				// Remove the old margin
				if (len > 3) {
					this.destroyMargin(this.margins.removeAt(indexLeft - 1));
				}

				// Add the new margins
				var margin1 = this.createMargin({
					path: [ pointLeft, newPoint ],

					index: indexLeft
				}), margin2 = this.createMargin({
					path: [ newPoint, pointRight ],

					index: index
				});

				this.margins.push(margin1);
				this.margins.insertAt(index, margin2);

				// Update all subsequent margins
				for (var marginsLength=this.margins.getLength(), i=index + 1; i<marginsLength; i++) {
					var margin = this.margins.getAt(i);

					margin.index = i;
				}
			}
			else if (index == len - 1) {
				var indexRight = 0, indexLeft = index - 1,
					pointRight = path.getAt(indexRight), pointLeft = path.getAt(indexLeft);
				
				// Remove the old margin
				if (len > 3) {
					this.destroyMargin(this.margins.removeAt(indexLeft));
				}

				// Add the new margins
				var margin1 = this.createMargin({
					path: [ pointLeft, newPoint ],

					index: indexLeft
				}), margin2 = this.createMargin({
					path: [ newPoint, pointRight ],

					index: index
				});

				this.margins.push(margin1);
				this.margins.push(margin2);
			}
			else {
				var indexRight = index + 1, indexLeft = index - 1,
					pointRight = path.getAt(indexRight), pointLeft = path.getAt(indexLeft);

				// Remove the old margin
				if (len > 3) {
					this.destroyMargin(this.margins.removeAt(indexLeft));
				}

				// Add the new margins
				var margin1 = this.createMargin({
					path: [ pointLeft, newPoint ],

					index: indexLeft
				}), margin2 = this.createMargin({
					path: [ newPoint, pointRight ],

					index: index
				});

				this.margins.insertAt(indexLeft, margin1);
				this.margins.insertAt(indexLeft + 1, margin2);

				// Update all subsequent margins
				for (var marginsLength=this.margins.getLength(), i=indexLeft + 1; i<marginsLength; i++) {
					var margin = this.margins.getAt(i);

					margin.index = i;
				}
			}
		}

		// Update the indexes of the subsequent points
		for (var i=index; i<len; i++) {
			path.getAt(i).index = i;
		}
	};

	/// @protected Handles when a point in the polygon's path is modified and adjusts the adiacent margins to the new point. 
	ObservablePolygon.prototype.onPathPointSet = function (index, point) {
		var path = this.getPath(), len = path.getLength(),
			newPoint = path.getAt(index),
			indexLeft = index == 0 ? len - 1 : index - 1, indexRight = index == len - 1 ? 0 : index + 1;

		var marginLeft = this.margins.getAt(indexLeft), marginRight = this.margins.getAt(index),
			pointLeft = path.getAt(indexLeft), pointRight = path.getAt(indexRight);

		marginLeft.setPath([ pointLeft, newPoint ]);
		marginRight.setPath([ newPoint, pointRight ]);

		// Update the point index
		newPoint.index = index;
	};

	/// @protected Handles when a point is removed from the path.
	ObservablePolygon.prototype.onPathPointRemoved = function (index) {
		var path = this.getPath(), len = path.getLength();

		if (len == 1) {
			this.destroyMargin(this.margins.removeAt(0));
		}
		else if (len == 2) {
			// Remove the margins
			var marginsLength = this.margins.getLength(), 
				indexLeft = index == 0 ? marginsLength - 2 : index - 1;

			this.destroyMargin(this.margins.removeAt(index));
			this.destroyMargin(this.margins.removeAt(indexLeft));

			// Update the last margin
			this.margins.getAt(0).index = 0;
		}
		else if (len > 2) {
			// Remove one of the margins
			this.destroyMargin(this.margins.removeAt(index));

			var marginsLength = this.margins.getLength(), 
				leftMarginIndex = index == 0 ? marginsLength - 1 : index - 1, margin = this.margins.getAt(leftMarginIndex),
				indexLeft = index == 0 ? len - 1 : index - 1, indexRight = index == len ? 0 : index,
				pointLeft = path.getAt(indexLeft), pointRight = path.getAt(indexRight);

			margin.setPath([ pointLeft, pointRight ]);

			// Update all subsequent margins
			for (var i=Math.min(indexLeft, indexRight); i<marginsLength; i++) {
				var margin = this.margins.getAt(i);

				margin.index = i;
			}
		}

		// Update the indexes of the subsequent points
		for (var i=index; i<len; i++) {
			path.getAt(i).index = i;
		}
	};

	ObservablePolygon.prototype.onMarginMouseMove = function (margin) {
		this.onMarginFocus(margin.index, margin);
	};
    ObservablePolygon.prototype.onMarginMouseMove = function (margin) {
		this.onMarginFocus(margin.index, margin);
	};

	/// @protected Fires the margin:focus event.
	ObservablePolygon.prototype.onMarginFocus = function (index, margin) {
        Gm.event.trigger(this, "margin:focus", index);
	};
    ObservablePolygon.prototype.onClick = function () {
        console.log('a')
	};

	return ObservablePolygon;
})(google.maps);