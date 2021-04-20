import os
import numpy as np
from typing import List, Tuple, Dict

# import ptvsd

from bokeh.layouts import column, row
from bokeh.models import (
    CustomJS,
    ColumnDataSource,
    Slider,
    RangeSlider,
    Select,
    Div,
    Paragraph,
    Tabs,
    Panel,
    Circle,
    Button,
    RadioButtonGroup,
)
from bokeh.models import (
    tools,
    HoverTool,
    Spacer,
    BoxZoomTool,
    ResetTool,
    PanTool,
    WheelZoomTool,
    SaveTool,
    TapTool,
    PrintfTickFormatter,
    Dropdown,
    InputWidget,
    CheckboxButtonGroup,
    FuncTickFormatter,
)
from bokeh.io import save, state
from bokeh.util.browser import view
from bokeh.plotting import Figure, output_file, show
from bokeh.models.callbacks import CustomJS
from bokeh.colors import Color, RGB

from Shared.Paths import PathsClass
from Illustration.BokehPlotFunctions.GenerateSmoothWarmColor import createColorArray


class BokehPlot:
    def __init__(
        self,
        paths: PathsClass,
        featureDetails: Dict[str, Tuple[str, str]],
        outputPath: str,
        absPath=False,
    ):
        # ptvsd.debug_this_thread()
        self.paths = paths
        self.featureDetails = featureDetails
        self.outputPath = outputPath
        self.name = outputPath.rpartition(os.path.sep)[2].replace(".html", "")
        self.__preferences__()
        self.namePicturePaths = "PicturePaths"
        self.namePartIDs = self.paths.part_id
        self.absPath = absPath

    def __preferences__(self):
        # global preferences
        self.toolbar_location = "above"
        self.plotWidth = 600
        self.plotHeight = 600
        self.widgetWidth = 200
        self.circleDiameter = 3.0
        self.sliderRangeSteps = 10

        self.bokehPath = os.path.dirname(os.path.abspath(__file__))

    def start(self, data: np.ndarray):
        self.data = data
        self.dataNames_Tuple = self.data.dtype.names

        self.constructBokeh()

    def constructBokeh(self):

        # preprocessing of data
        self.editData()

        # define plot data container
        self.plotContainer()

        # definition of widgets
        controlColumn = self.defineControlWidgets()
        # java output
        self.div = Div(width=400, height=self.plotHeight, height_policy="fixed")

        self.dataTabs = Tabs(
            tabs=self.scatterTabBuilder(), width=self.plotWidth, height=self.plotHeight
        )

        self.interactiveFunctions()

        layout = row(
            self.dataTabs, Spacer(width=20), controlColumn
        )  # , Spacer(width=20), self.div)

        fileState = state.State()
        fileState.output_file(self.outputPath, title=self.name, mode="inline")
        save(layout, state=fileState)
        # view(self.outputPath)

    def editData(self):
        # number of parts
        self.numberOfParts = self.data[self.dataNames_Tuple[0]].shape[0]

        self.bokehDataNames_List = []
        for colName in self.dataNames_Tuple:
            typeCol = self.data.dtype[colName].type
            if typeCol != np.bytes_:
                self.bokehDataNames_List.append(colName)

        # select float data
        bokehDataDict = {}
        bokehFormatDict = {}
        self.bokehDataNameOutput_list = []
        for bokehDataName in self.bokehDataNames_List:
            colName = self.featureDetails[bokehDataName][0]
            colFormat = self.featureDetails[bokehDataName][1]
            self.bokehDataNameOutput_list.append(colName)
            bokehDataDict[colName] = self.data[bokehDataName]
            bokehFormatDict[colName] = [colFormat]

        # define start data
        self.startDataName_x = self.bokehDataNameOutput_list[0]
        self.startDataName_y = self.bokehDataNameOutput_list[1]

        # define start radius
        self.columnStartRadius = "Start Radius"
        bokehDataDict[self.columnStartRadius] = np.full(
            self.numberOfParts, self.circleDiameter
        )
        bokehDataDict["r"] = bokehDataDict[self.columnStartRadius]

        # define chronological part IDs
        self.columnIDs = "Chronological body numbering"
        bokehDataDict[self.columnIDs] = range(0, self.numberOfParts, 1)
        self.bokehDataNameOutput_list = [self.columnIDs] + self.bokehDataNameOutput_list

        # define part colors
        self.columnStartColor = "Start Color"
        self.startColor = RGB(127, 127, 127).to_hex()
        bokehDataDict[self.columnStartColor] = np.full(
            self.numberOfParts, self.startColor
        )
        bokehDataDict["c"] = bokehDataDict[self.columnStartColor]

        # define color array
        colorArray = self.defineColorArray(1024)
        self.bokehColors = ColumnDataSource(data={"Colors": colorArray})

        self.bokehFeatureData = ColumnDataSource(data=bokehDataDict)
        self.bokehFormatFeatures = ColumnDataSource(data=bokehFormatDict)

    def plotContainer(self):
        self.bokehPlotData = ColumnDataSource()
        self.bokehPlotData.add(self.bokehFeatureData.data[self.startDataName_x], "x")
        self.bokehPlotData.add(self.bokehFeatureData.data[self.startDataName_y], "y")
        self.bokehPlotData.add(self.bokehFeatureData.data[self.columnStartRadius], "r")
        self.bokehPlotData.add(self.bokehFeatureData.data[self.columnStartColor], "c")
        array1 = np.full(self.numberOfParts, 1.0)
        self.bokehPlotData.add(array1, "rFloats")
        self.bokehPlotData.add(array1, "cFloats")
        self.bokehPlotData.add(np.arange(0, self.numberOfParts, 1), "index")

        # take part IDs
        decodedPartIDs = np.char.decode(self.data[self.paths.part_id], "utf-8")
        self.bokehFeatureData.add(decodedPartIDs, self.paths.part_id)
        self.bokehPlotData.add(decodedPartIDs, self.paths.part_id)

        # paths to physical part directory for pictures
        pathArray = np.empty(self.numberOfParts, dtype=object)
        for i, name in enumerate(self.data[self.paths.part_id]):
            nameSplit = name.decode("utf-8").rpartition("_")
            assemblyID, partID = (nameSplit[0], nameSplit[2])
            if self.absPath == False:
                pathArray[i] = "./" + os.path.join(
                    self.paths.name_physicaldatabase,
                    assemblyID,
                    partID,
                    partID + "_" + self.paths.namedata_image,
                ).replace("\\", "/")
            else:
                pathArray[i] = os.path.join(
                    self.paths.path_physicaldatabase,
                    assemblyID,
                    partID,
                    partID + "_" + self.paths.namedata_image,
                ).replace("\\", "/")
        self.bokehFeatureData.add(pathArray, self.namePicturePaths)
        self.bokehPlotData.add(pathArray, self.namePicturePaths)

    def defineControlWidgets(self):

        captionSelection = Paragraph(text="Data Selection", height=20)
        self.categories_X = Select(
            title="X-Axis",
            value=self.startDataName_x,
            options=self.bokehDataNameOutput_list,
        )
        dataX = self.bokehPlotData.data["x"]
        xMin = np.min(dataX)
        xMax = np.max(dataX)
        if xMax == xMin:
            xMin = xMax - 1

        self.slider_rangeX = RangeSlider(
            start=xMin,
            end=xMax,
            value=(xMin, xMax),
            step=(xMax - xMin) / self.sliderRangeSteps,
            title="Show X in range",
            name="x",
            show_value=False,
        )

        self.categories_Y = Select(
            title="Y-Axis",
            value=self.startDataName_y,
            options=self.bokehDataNameOutput_list,
        )

        dataY = self.bokehPlotData.data["y"]
        yMin = np.min(dataY)
        yMax = np.max(dataY)
        if yMax == yMin:
            yMin = yMax - 1

        self.slider_rangeY = RangeSlider(
            start=yMin,
            end=yMax,
            value=(yMin, yMax),
            step=(yMax - yMin) / self.sliderRangeSteps,
            title="Show Y in range",
            name="y",
            show_value=False,
        )

        widgetBoxDataSelection = column(
            [
                self.categories_X,
                self.slider_rangeX,
                Spacer(height=10),
                self.categories_Y,
                self.slider_rangeY,
            ],
            width=self.widgetWidth,
        )

        self.categories_R = Select(
            title="Radius",
            value=self.columnStartRadius,
            options=[self.columnStartRadius] + self.bokehDataNameOutput_list,
        )

        dataR = self.bokehPlotData.data["r"]
        rMin = np.min(dataR)
        rMax = np.max(dataR)
        if rMax == rMin:
            rMin = rMax - 1

        self.slider_rangeR = RangeSlider(
            start=rMin,
            end=rMax,
            value=(rMin, rMax),
            step=(rMax - rMin) / self.sliderRangeSteps,
            title="Show Radius in range",
            name="r",
            show_value=False,
        )

        self.slider_scalingR = Slider(
            start=0.0, end=1.0, value=0.0, step=0.1, title="Scaling of Radius"
        )

        widgetBoxDataRadius = column(
            [self.categories_R, self.slider_rangeR, self.slider_scalingR],
            width=self.widgetWidth,
        )

        self.categories_C = Select(
            title="Coloring",
            value=self.columnStartColor,
            options=[self.columnStartColor] + self.bokehDataNameOutput_list,
            tags=["ColoringClass"],
        )

        dataC = self.bokehPlotData.data["cFloats"]
        cMin = np.min(dataC)
        cMax = np.max(dataC)
        if cMax == cMin:
            cMin = cMax - 1

        self.slider_rangeC = RangeSlider(
            start=cMin,
            end=cMax,
            value=(cMin, cMax),
            step=(cMax - cMin) / self.sliderRangeSteps,
            title="Show Color in range",
            name="cFloats",
            show_value=False,
        )

        self.RadioButtonColorFunctions = RadioButtonGroup(
            labels=["-quad", "lin", "+quad"],
            tags=["ColoringFunction"],
            active=1,
            orientation="horizontal",
        )
        widgetBoxColor = column(
            [self.categories_C, self.slider_rangeC, self.RadioButtonColorFunctions],
            width=self.widgetWidth,
        )

        controlColumn = column(
            captionSelection,
            widgetBoxDataSelection,
            Spacer(height=10),
            widgetBoxDataRadius,
            Spacer(height=10),
            widgetBoxColor,
        )

        return controlColumn

    def scatterTabBuilder(self):

        toolsDefinition = [
            PanTool(),
            WheelZoomTool(),
            BoxZoomTool(),
            ResetTool(),
            self.customHoverTool(),
            SaveTool(),
        ]

        self.X_Axis_List = []
        self.Y_Axis_List = []

        tab_1 = self.buildScatterPlot(
            self.plotWidth,
            self.plotHeight,
            "CAD - Feature Data",
            ("linear", "linear"),
            toolsDefinition,
            (50, 0, 0, 0),
        )

        tab_2 = self.buildScatterPlot(
            self.plotWidth,
            self.plotHeight,
            "CAD - Feature Data",
            ("log", "linear"),
            toolsDefinition,
            (50, 0, 0, 0),
        )

        tab_3 = self.buildScatterPlot(
            self.plotWidth,
            self.plotHeight,
            "CAD - Feature Data",
            ("linear", "log"),
            toolsDefinition,
            (50, 0, 0, 0),
        )

        tab_4 = self.buildScatterPlot(
            self.plotWidth,
            self.plotHeight,
            "CAD - Feature Data",
            ("log", "log"),
            toolsDefinition,
            (50, 0, 0, 0),
        )

        return [tab_1, tab_2, tab_3, tab_4]

    def customPointTooltip(self) -> str:

        info_script = """
        <table align="center">
            <col width="150" />
            <col width="50" />
            <tr>
                <th>
                    <img
                        src="@{0}" height="150" alt="@{0}" width="150"
                        style="float: top; margin: 0px 0px 0px 0px;"
                    ></img>
                </th>
                <th align="left">
                    <div>
                        <span style="font-size: 17px; color: #000;">Values</span><br>
                        <span style="font-size: 15px; color: #808080;">X=@x</span><br>
                        <span style="font-size: 15px; color: #808080;">Y=@y</span><br>
                        <span style="font-size: 15px; color: #808080;">Radius=@rFloats</span><br>
                        <span style="font-size: 15px; color: #808080;">Color=@cFloats</span>
                    </div>
                </th>
            </tr>
            </tr>
                <th colspan="2">
                    <span style="font-size: 17px; color: #000;">@{1}</span>
                </th>
            </tr>
        </table>
        """.format(
            self.namePicturePaths, self.namePartIDs
        )
        return info_script

    def customHoverTool(self) -> HoverTool:
        return HoverTool(tooltips=self.customPointTooltip())

    def buildScatterPlot(
        self,
        width: float,
        height: float,
        name: str,
        type_in: Tuple[str, str],
        tools: List,
        borders: Tuple[float, float, float, float] = (0, 0, 0, 0),
    ):
        """order of boarders: left, bottom, right, top"""

        # main figure
        fig_main = Figure(
            plot_width=width,
            plot_height=height,
            title=name,
            x_axis_type=type_in[0],
            y_axis_type=type_in[1],
            tools=tools,
            toolbar_location=self.toolbar_location,
            min_border_left=borders[0],
            min_border_bottom=borders[1],
            min_border_right=borders[2],
            min_border_top=borders[3],
        )

        # scatter data
        fig_main_scatter = fig_main.scatter(
            "x",
            "y",
            size="r",
            fill_color="c",
            source=self.bokehPlotData,
            line_color="black",
            line_width=0.5,
        )

        fig_main.xaxis.axis_label = self.startDataName_x
        fig_main.yaxis.axis_label = self.startDataName_y

        if self.bokehFormatFeatures.data[self.startDataName_x][0] == "lin":
            fig_main.xaxis[0].formatter = FuncTickFormatter(
                code="""return tick.toExponential()"""
            )
        else:
            fig_main.xaxis[0].formatter = FuncTickFormatter(
                code="""return (tick * 100).toFixed(0) + '%'"""
            )
        if self.bokehFormatFeatures.data[self.startDataName_y][0] == "lin":
            fig_main.yaxis[0].formatter = FuncTickFormatter(
                code="""return tick.toExponential()"""
            )
        else:
            fig_main.yaxis[0].formatter = FuncTickFormatter(
                code="""return (tick * 100).toFixed(0) + '%'"""
            )

        self.X_Axis_List.append(fig_main.xaxis[0])
        self.Y_Axis_List.append(fig_main.yaxis[0])

        tab_main = Panel(
            child=fig_main, title="X {}, Y {}".format(type_in[0], type_in[1])
        )
        return tab_main

    def interactiveFunctions(self):

        self.categories_X.js_on_change("value", self.callback_dataChange())
        self.categories_Y.js_on_change("value", self.callback_dataChange())

        self.categories_R.js_on_change("value", self.callback_radiusChange())
        self.slider_scalingR.js_on_change(
            "value_throttled", self.callback_radiusChange()
        )

        self.categories_C.js_on_change("value", self.callback_colorDataChange())

        self.RadioButtonColorFunctions.js_on_change(
            "active", self.callback_colorDataChange()
        )

        self.slider_rangeX.js_on_change(
            "value_throttled",
            self.callback_sliderChange(),
            self.callback_radiusChange(),
            self.callback_colorDataChange(),
        )
        self.slider_rangeY.js_on_change(
            "value_throttled",
            self.callback_sliderChange(),
            self.callback_radiusChange(),
            self.callback_colorDataChange(),
        )
        self.slider_rangeR.js_on_change(
            "value_throttled",
            self.callback_sliderChange(),
            self.callback_radiusChange(),
            self.callback_colorDataChange(),
        )
        self.slider_rangeC.js_on_change(
            "value_throttled",
            self.callback_sliderChange(),
            self.callback_radiusChange(),
            self.callback_colorDataChange(),
        )

    def callback_dataChange(self):

        stringFile = open(os.path.join(self.bokehPath, "DataChange.js"), "r")

        javaString = stringFile.read()
        stringFile.close()

        changeJS = CustomJS(
            args=dict(
                bokehPlotDataIn=self.bokehPlotData,
                bokehFeatureDataIn=self.bokehFeatureData,
                bokehFormatFeaturesIn=self.bokehFormatFeatures,
                categories_X=self.categories_X,
                categories_Y=self.categories_Y,
                X_Axis_List=self.X_Axis_List,
                Y_Axis_List=self.Y_Axis_List,
                X_Slider=self.slider_rangeX,
                Y_Slider=self.slider_rangeY,
                divIn=self.div,
            ),
            code=javaString,
        )
        return changeJS

    def callback_radiusChange(self):

        stringFile = open(os.path.join(self.bokehPath, "RadiusChange.js"), "r")

        javaString = stringFile.read()
        stringFile.close()

        changeJS = CustomJS(
            args=dict(
                bokehPlotDataIn=self.bokehPlotData,
                bokehFeatureDataIn=self.bokehFeatureData,
                categories_R=self.categories_R,
                slider_scalingR=self.slider_scalingR,
                startRadiusIn=self.circleDiameter,
                sliderRangeXIn=self.slider_rangeX,
                sliderRangeYIn=self.slider_rangeY,
                sliderRangeRIn=self.slider_rangeR,
                sliderRangeCIn=self.slider_rangeC,
                divIn=self.div,
            ),
            code=javaString,
        )
        return changeJS

    def callback_colorDataChange(self,):

        stringFile = open(os.path.join(self.bokehPath, "ColorChange.js"), "r")

        javaString = stringFile.read()
        stringFile.close()

        changeJS = CustomJS(
            args=dict(
                bokehPlotDataIn=self.bokehPlotData,
                bokehDataIn=self.bokehFeatureData,
                bokehColorsIn=self.bokehColors,
                startColorIn=self.startColor,
                categoryColorIn=self.categories_C,
                distanceFunctionIn=self.RadioButtonColorFunctions,
                sliderRangeCIn=self.slider_rangeC,
                divIn=self.div,
            ),
            code=javaString,
        )
        return changeJS

    def callback_sliderChange(self):

        stringFile = open(os.path.join(self.bokehPath, "SliderChange.js"), "r")

        javaString = stringFile.read()
        stringFile.close()

        changeJS = CustomJS(
            args=dict(
                bokehFeatureDataIn=self.bokehFeatureData,
                bokehPlotDataIn=self.bokehPlotData,
                sliderRangeXIn=self.slider_rangeX,
                sliderRangeYIn=self.slider_rangeY,
                sliderRangeRIn=self.slider_rangeR,
                sliderRangeCIn=self.slider_rangeC,
                categoryXIn=self.categories_X,
                categoryYIn=self.categories_Y,
                categoryRIn=self.categories_R,
                categoryCIn=self.categories_C,
                dataNamesIn=[self.namePicturePaths, self.namePartIDs],
                divIn=self.div,
            ),
            code=javaString,
        )
        return changeJS

    def defineColorArray(self, count=2) -> np.ndarray:
        colorArray = createColorArray(count)
        RGBarray = np.empty((count,), dtype=object)
        for i, color in enumerate(colorArray):
            RGBarray[i] = RGB(color[0], color[1], color[2]).to_hex()

        return RGBarray
