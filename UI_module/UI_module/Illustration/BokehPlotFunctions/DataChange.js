// JavaScript code goes here

// plot container
var bokehPlotData = bokehPlotDataIn.data;
// data
var bokehFeatureData = bokehFeatureDataIn.data;
// format
var bokehFormatFeatures = bokehFormatFeaturesIn.data;

// widgets
var catX = categories_X
var catY = categories_Y

// xAxis and yAxis list
var xAxes = X_Axis_List
var yAxes = Y_Axis_List

// sliders x and y
var xSlider = X_Slider
var ySlider = Y_Slider

// the model that triggered the callback is cb_obj:
var inputValue = cb_obj.value;
var inputName = cb_obj.title;

// div, java output
var div = divIn
div.text = ""

// models passed as args are automagically available

var dataCategory = bokehFeatureData[inputValue];
var min = Math.min(...dataCategory);
var max = Math.max(...dataCategory);
if (min == max) {
    min = max - 1
}

if (inputName == "X-Axis") {

    for (var i = 0; i < xAxes.length; i++) {
        xAxes[i].axis_label = inputValue;
        div.text += bokehFormatFeatures[inputValue][0]
        xAxes[i].formatter.code = "return tick.toExponential()"
        if (bokehFormatFeatures[inputValue][0] == "per") {
            div.text += "Change"
            xAxes[i].formatter.code = "return (tick * 100).toFixed(0) + '%' "
        }
    }

    if (bokehPlotData["index"].length != dataCategory.length) {
        for (var i = 0; i < bokehPlotData["index"].length; i++) {
            var index = bokehPlotData["index"][i]
            var value_cat = dataCategory[index]
            bokehPlotData["x"][i] = value_cat
        }
    }
    else {
        bokehPlotData["x"] = dataCategory;
    }

    // first dummy values -> end == start = Error
    xSlider.start = -10e3 + 1234e-5
    xSlider.end = +10e3 + 1234e-5
    xSlider.start = min;
    xSlider.end = max;
    xSlider.value[0] = min
    xSlider.value[1] = max
    xSlider.step = (max - min) / 10
}

if (inputName == "Y-Axis") {
    for (var i = 0; i < yAxes.length; i++) {
        yAxes[i].axis_label = inputValue;
        div.text += bokehFormatFeatures[inputValue][0]
        yAxes[i].formatter.code = "return tick.toExponential()"
        if (bokehFormatFeatures[inputValue][0] == "per") {
            div.text += "Change"
            yAxes[i].formatter.code = "return (tick * 100).toFixed(0) + '%' "
        }
    }

    if (bokehPlotData["index"].length != dataCategory.length) {
        for (var i = 0; i < bokehPlotData["index"].length; i++) {
            var index = bokehPlotData["index"][i]
            var value_cat = dataCategory[index]
            bokehPlotData["y"][i] = value_cat
        }
    }
    else {
        bokehPlotData["y"] = dataCategory;
    }
    // first dummy values -> end == start = Error
    ySlider.start = -10e3 + 1234e-5
    ySlider.end = +10e3 + 1234e-5
    ySlider.start = min;
    ySlider.end = max;
    ySlider.value[0] = min
    ySlider.value[1] = max
    ySlider.step = (max - min) / 10
}

X_Slider.change.emit()
Y_Slider.change.emit()
bokehPlotDataIn.change.emit()