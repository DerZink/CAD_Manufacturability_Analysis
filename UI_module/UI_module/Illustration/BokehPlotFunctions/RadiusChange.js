// JavaScript code goes here

// plot container
var bokehPlotData = bokehPlotDataIn.data;

// data
var bokehFeatureData = bokehFeatureDataIn.data;

// start radius
var startRadius = startRadiusIn

// widgets
var catR = categories_R
var sliR = slider_scalingR
// sliders
var sliX = sliderRangeXIn;
var sliY = sliderRangeYIn;
var sliRR = sliderRangeRIn;
var sliC = sliderRangeCIn;

// div, java output
var div = divIn

// the model that triggered the callback is cb_obj:
var inputTitle = cb_obj.title;

var r_min = startRadius;
var r_objective = 20;
var r_gradient = r_objective - r_min;
var r_max_abs = 30;
var r_max_grad = -(r_max_abs - r_gradient) * (1.0 - sliR.value) + r_max_abs;

var radiusSelectedCategory = catR.value;


if (radiusSelectedCategory == "Start Radius") {
    for (var i = 0; i < bokehPlotData["index"].length; i++) {
        bokehPlotData["rFloats"][i] = 1.0
        bokehPlotData["r"][i] = (r_max_abs - r_min) / (1.0) * sliR.value + r_min;
    }
    if (inputTitle == "Radius") {
        // first dummy values -> end == start = Error
        sliRR.start = -10e3 + 1234e-5
        sliRR.end = +10e3 + 1234e-5
        sliRR.start = startRadius - 1;
        sliRR.end = startRadius;
        sliRR.value[0] = sliRR.start
        sliRR.value[1] = sliRR.end
        sliRR.step = 1 / 10
    }
}
else {

    var dataCategory = bokehFeatureData[radiusSelectedCategory];
    var dataMin = Math.min(...dataCategory);
    var dataMax = Math.max(...dataCategory);
    var deltaData = dataMax - dataMin;

    if (inputTitle == "Radius") {
        // first dummy values -> end == start = Error
        sliRR.start = -10e3 + 1234e-5
        sliRR.end = +10e3 + 1234e-5
        sliRR.end = dataMax;
        if (deltaData == 0) {
            sliRR.start = dataMax - 1
        }
        else {
            sliRR.start = dataMin;

        }
        sliRR.value[0] = sliRR.start
        sliRR.value[1] = sliRR.end
        sliRR.step = (sliRR.end - sliRR.start) / 10
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
    var gradientData = 0;
    if (deltaData != 0) {
        gradientData = r_max_grad / deltaData;
        for (var i = 0; i < bokehPlotData["index"].length; i++) {
            var index = bokehPlotData["index"][i]
            var value_cat = dataCategory[index]
            bokehPlotData["rFloats"][i] = value_cat
            bokehPlotData["r"][i] = gradientData * (value_cat - dataMin) + r_min;
        }
    }
    else {
        for (var i = 0; i < bokehPlotData["index"].length; i++) {
            bokehPlotData["rFloats"][i] = dataMin
            bokehPlotData["r"][i] = (r_max_abs - r_min) / (1.0) * sliR.value + r_min
        }
    }
}

sliderRangeRIn.change.emit();
bokehPlotDataIn.change.emit();