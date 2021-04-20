// JavaScript code goes here

// feature data container
var bokehFeatureData = bokehFeatureDataIn.data;
// plot container
var bokehPlotData = bokehPlotDataIn.data;

// widgets
// sliders
var sliX = sliderRangeXIn;
var sliY = sliderRangeYIn;
var sliR = sliderRangeRIn;
var sliC = sliderRangeCIn;
// categories
var catX = categoryXIn;
var catY = categoryYIn;
var catR = categoryRIn;
var catC = categoryCIn;

// data names
var names = dataNamesIn;
var namePicturePaths = names[0];
var namePartIDs = names[1];

// input slider
var inputName = cb_obj.name;

// div, java output
var div = divIn;

var cats = [{ name: "x", slider: sliX, cat: catX }, { name: "y", slider: sliY, cat: catY }, { name: "r", slider: sliR, cat: catR }, { name: "cFloats", slider: sliC, cat: catC }]

bokehPlotData["x"] = []
bokehPlotData["y"] = []
bokehPlotData["r"] = []
bokehPlotData["c"] = []
bokehPlotData[namePartIDs] = []
bokehPlotData[namePicturePaths] = []

var indexNew = []
for (var i = 0; i < bokehFeatureData[catX.value].length; i++) {

    var valueChecks = true
    for (var c = 0; c < cats.length; c++) {

        var catPlot = cats[c];
        var catData = catPlot.cat.value
        var valueInCat = bokehFeatureData[catData][i]

        if (valueInCat < catPlot.slider.value[0] || valueInCat > catPlot.slider.value[1]) {
            valueChecks = false
            break
        }
    }

    if (valueChecks == true) {
        indexNew.push(i)
        bokehPlotData["x"].push(bokehFeatureData[catX.value][i])
        bokehPlotData["y"].push(bokehFeatureData[catY.value][i])
        bokehPlotData["r"].push(bokehFeatureData[catR.value][i])
        bokehPlotData["c"].push(bokehFeatureData[catC.value][i])
        bokehPlotData[namePartIDs].push(bokehFeatureData[namePartIDs][i])
        bokehPlotData[namePicturePaths].push(bokehFeatureData[namePicturePaths][i])
    }
}
bokehPlotData["index"] = indexNew
bokehPlotDataIn.change.emit()