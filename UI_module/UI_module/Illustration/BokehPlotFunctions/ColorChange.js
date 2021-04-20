// JavaScript code goes here
// plot container
var bokehPlotData = bokehPlotDataIn.data;

// data
var bokehFeatureData = bokehDataIn.data;

// color array
var bokehColors = bokehColorsIn.data["Colors"]

// start color
var startColor = startColorIn

// current data category
var colorSelectedCategory = categoryColorIn.value


// current tab title
var positionButton = distanceFunctionIn.active;
var distanceFunction = distanceFunctionIn.labels[positionButton]

// color slider
var sliC = sliderRangeCIn

// the model that triggered the callback is cb_obj:
var inputTitle = cb_obj.tags[0];

// div, java output
var div = divIn

if (colorSelectedCategory == "Start Color") {
    for (var i = 0; i < bokehPlotData["index"].length; i++) {
        bokehPlotData["c"][i] = startColor;
        bokehPlotData["cFloats"][i] = 1.0;
    }

    if (inputTitle == "ColoringClass") {
        // first dummy values -> end == start = Error
        sliC.start = -10e3 + 1234e-5
        sliC.end = +10e3 + 1234e-5
        sliC.start = 0;
        sliC.end = 1;
        sliC.value[0] = sliC.start
        sliC.value[1] = sliC.end
        sliC.step = 1 / 10
    }
}
else {
    var dataCategory = bokehFeatureData[colorSelectedCategory];
    var dataMin = Math.min(...dataCategory);
    var dataMax = Math.max(...dataCategory);
    var deltaData = dataMax - dataMin;

    if (inputTitle == "ColoringClass") {
        // first dummy values -> end == start = Error
        sliC.start = -10e3 + 1234e-5
        sliC.end = +10e3 + 1234e-5
        sliC.end = dataMax
        if (deltaData == 0) {
            sliC.start = sliC.end - 1
        }
        else {
            sliC.start = dataMin
        }
        sliC.value[0] = sliC.start
        sliC.value[1] = sliC.end
        sliC.step = (sliC.end - sliC.start) / 10
    }

    if (bokehPlotData["index"].length != dataCategory.length) {
        var minGlobal = Infinity
        var maxGlobal = 0.0
        for (var i = 0; i < bokehPlotData["index"].length; i++) {
            var index = bokehPlotData["index"][i]
            var value_cat = dataCategory[index]
            if (value_cat < minGlobal) {
                minGlobal = value_cat
            }
            if (value_cat > maxGlobal) {
                maxGlobal = value_cat
            }
        }

        dataMin = minGlobal;
        dataMax = maxGlobal;
        deltaData = dataMax - dataMin;
    }

    if (deltaData != 0.0) {
        var a = 0.0;
        var b = (bokehColors.length - 1) / (dataMax - dataMin);
        var c = -1 * b * dataMin;

        if (distanceFunction == "-quad") {
            var a = -(bokehColors.length - 1) / (Math.pow(dataMax, 2) - 2 * dataMin * dataMax + Math.pow(dataMin, 2));
            var b = -2 * a * dataMax;
            var c = a * Math.pow(dataMax, 2) + (bokehColors.length - 1)
        }
        else if (distanceFunction == "+quad") {
            var a = (bokehColors.length - 1) / (Math.pow(dataMax, 2) - 2 * dataMin * dataMax + Math.pow(dataMin, 2));
            var b = -2 * a * dataMin;
            var c = a * Math.pow(dataMin, 2)
        }

        for (var i = 0; i < bokehPlotData["index"].length; i++) {
            var index = bokehPlotData["index"][i]
            var value_i = dataCategory[index]
            bokehPlotData["cFloats"][i] = value_i;
            var arrayPosition = Math.round(a * Math.pow(value_i, 2) + b * value_i + c);
            bokehPlotData["c"][i] = bokehColors[arrayPosition];
        }

    }
    else {
        for (var i = 0; i < bokehPlotData["index"].length; i++) {
            bokehPlotData["c"][i] = startColor
            bokehPlotData["cFloats"][i] = dataMin
        }
    }
}
sliderRangeCIn.change.emit()
bokehPlotDataIn.change.emit();