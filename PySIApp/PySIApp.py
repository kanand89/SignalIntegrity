from Tkinter import *

from tkFileDialog import askopenfilename
from tkFileDialog import asksaveasfilename
from tkFileDialog import askdirectory
import tkMessageBox
import copy
import os

from PartPin import *
from PartPicture import *
from PartProperty import *
from Device import *
from DeviceProperties import *
from DevicePicker import *
from Schematic import *
from PlotWindow import *
from CalculationProperties import *
from Simulator import *
from NetList import *
from SParameterViewerWindow import *
from Files import *
from History import *
from MenuSystemHelpers import *

class TheApp(Frame):
    def __init__(self):
        self.root = Tk()
        Frame.__init__(self, self.root)
        self.pack(fill=BOTH, expand=YES)

        self.root.title("PySI")

        img = PhotoImage(file='./icons/png/AppIcon2.gif')
        self.root.tk.call('wm', 'iconphoto', self.root._w, '-default', img)

        sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/..')
        foundSignalIntegrity=False
        while not foundSignalIntegrity:
            foundSignalIntegrity = True
            try:
                import SignalIntegrity as si
            except ImportError:
                foundSignalIntegrity = False
                if tkMessageBox.askokcancel('SignalIntegrity Package',
                    'In order to run this application, I need to know where the '+\
                    'SignalIntegrity package is.  Please browse to the directory where '+\
                    'it\'s installed.\n'+'You should only need to do this once'):
                        dirname = askdirectory(parent=self.root,initialdir=os.path.dirname(os.path.abspath(__file__)),
                            title='Please select a directory')
                        sys.path.append(dirname)
                else:
                    exit()

        # status bar
        self.statusbar=StatusBar(self)

        # the Doers - the holder of the commands, menu elements, toolbar elements, and key bindings
        self.OpenProjectDoer = Doer(self.onReadProjectFromFile).AddKeyBindElement(self.root,'<Control-o>').AddHelpElement('help_open_project')
        self.SaveProjectDoer = Doer(self.onWriteProjectToFile).AddKeyBindElement(self.root,'<Control-s>').AddHelpElement('help_save_project')
        self.ClearProjectDoer = Doer(self.onClearSchematic).AddHelpElement('help_clear_schematic')
        self.ExportNetListDoer = Doer(self.onExportNetlist).AddHelpElement('help_export_netlist')
        self.ExportTpXDoer = Doer(self.onExportTpX).AddHelpElement('help_export_latex')
        # ------
        self.UndoDoer = Doer(self.onUndo).AddKeyBindElement(self.root,'<Control-z>').AddHelpElement('help_undo')
        self.RedoDoer = Doer(self.onRedo).AddKeyBindElement(self.root,'<Control-Z>').AddHelpElement('help_redo')
        self.DeleteSelectedDoer = Doer(self.onDeleteSelected).AddKeyBindElement(self.root,'<Delete>').AddHelpElement('help_delete_selected')
        self.DuplicateSelectedDoer = Doer(self.onDuplicateSelected).AddKeyBindElement(self.root,'<Control-c>').AddHelpElement('help_duplicate_selected')
        self.CutSelectedDoer = Doer(self.onCutMultipleSelections).AddKeyBindElement(self.root,'<Control-x>').AddHelpElement('help_cut_selected')
        # ------
        self.AddPartDoer = Doer(self.onAddPart).AddHelpElement('help_add_part')
        self.AddPortDoer = Doer(self.onAddPort).AddHelpElement('help_add_port')
        self.AddMeasureProbeDoer = Doer(self.onAddMeasureProbe).AddHelpElement('help_add_measure_probe')
        self.AddOutputProbeDoer = Doer(self.onAddOutputProbe).AddHelpElement('help_add_output_probe')
        self.AddStimDoer = Doer(self.onAddStim).AddHelpElement('help_add_stim')
        self.AddUnknownDoer = Doer(self.onAddUnknown).AddHelpElement('help_add_unknown')
        self.AddSystemDoer = Doer(self.onAddSystem).AddHelpElement('help_add_system')
        self.DeletePartDoer = Doer(self.onDeletePart).AddHelpElement('help_delete_part')
        self.EditPropertiesDoer = Doer(self.onEditProperties)
        self.DuplicatePartDoer = Doer(self.onDuplicate)
        self.RotatePartDoer = Doer(self.onRotatePart)
        self.FlipPartHorizontallyDoer = Doer(self.onFlipPartHorizontally)
        self.FlipPartVerticallyDoer = Doer(self.onFlipPartVertically)
        # ------
        self.AddWireDoer = Doer(self.onAddWire)
        self.DeleteVertexDoer = Doer(self.onDeleteSelectedVertex)
        self.DuplicateVertexDoer = Doer(self.onDuplicateSelectedVertex)
        self.DeleteWireDoer = Doer(self.onDeleteSelectedWire)
        # ------
        self.ZoomInDoer = Doer(self.onZoomIn)
        self.ZoomOutDoer = Doer(self.onZoomOut)
        self.PanDoer = Doer(self.onPan)
        # ------
        self.CalculationPropertiesDoer = Doer(self.onCalculationProperties)
        self.SParameterViewerDoer = Doer(self.onSParameterViewer)
        self.CalculateDoer = Doer(self.onCalculate)
        self.CalculateSParametersDoer = Doer(self.onCalculateSParameters)
        self.VirtualProbeDoer = Doer(self.onVirtualProbe)
        self.SimulateDoer = Doer(self.onSimulate)
        self.DeembedDoer = Doer(self.onDeembed)
        # ------
        self.HelpDoer = Doer(self.onHelp)
        self.ControlHelpDoer = Doer(self.onControlHelp)
        # ------
        self.EscapeDoer = Doer(self.onEscape).AddKeyBindElement(self.root, '<Escape>').DisableHelp()

        # The menu system
        TheMenu=Menu(self.root)
        self.root.config(menu=TheMenu)
        FileMenu=Menu(self)
        TheMenu.add_cascade(label='File',menu=FileMenu,underline=0)
        self.OpenProjectDoer.AddMenuElement(FileMenu,label="Open Project",accelerator='Ctrl+O',underline=0)
        self.SaveProjectDoer.AddMenuElement(FileMenu,label="Save Project",accelerator='Ctrl+S',underline=0)
        FileMenu.add_separator()
        self.ClearProjectDoer.AddMenuElement(FileMenu,label="Clear Schematic",underline=0)
        FileMenu.add_separator()
        self.ExportNetListDoer.AddMenuElement(FileMenu,label="Export NetList",underline=7)
        self.ExportTpXDoer.AddMenuElement(FileMenu,label="Export LaTeX (TikZ)",underline=7)
        # ------
        EditMenu=Menu(self)
        TheMenu.add_cascade(label='Edit',menu=EditMenu,underline=0)
        self.UndoDoer.AddMenuElement(EditMenu,label="Undo",accelerator='Ctrl+Z', underline=0)
        self.RedoDoer.AddMenuElement(EditMenu,label="Redo",accelerator='Ctrl+Shift+Z',underline=0)
        EditMenu.add_separator()
        # ------
        self.DeleteSelectedDoer.AddMenuElement(EditMenu,label='Delete Selected',accelerator='Del',underline=0)
        self.DuplicateSelectedDoer.AddMenuElement(EditMenu,label='Duplicate Selected',accelerator='Ctrl+C',underline=1)
        self.CutSelectedDoer.AddMenuElement(EditMenu,label='Cut Selected',accelerator='Ctrl+X',underline=0)
        # ------
        PartsMenu=Menu(self)
        TheMenu.add_cascade(label='Parts',menu=PartsMenu,underline=0)
        self.AddPartDoer.AddMenuElement(PartsMenu,label='Add Part',underline=0)
        self.AddPortDoer.AddMenuElement(PartsMenu,label='Add Port',underline=6)
        self.AddOutputProbeDoer.AddMenuElement(PartsMenu,label='Add Output Probe',underline=4)
        self.AddMeasureProbeDoer.AddMenuElement(PartsMenu,label='Add Measure Probe',underline=4)
        self.AddStimDoer.AddMenuElement(PartsMenu,label='Add Stim',underline=5)
        self.AddUnknownDoer.AddMenuElement(PartsMenu,label='Add Unknown',underline=4)
        self.AddSystemDoer.AddMenuElement(PartsMenu,label='Add System',underline=4)
        PartsMenu.add_separator()
        self.DeletePartDoer.AddMenuElement(PartsMenu,label='Delete Part',underline=0)
        PartsMenu.add_separator()
        self.EditPropertiesDoer.AddMenuElement(PartsMenu,label='Edit Properties',underline=0)
        self.DuplicatePartDoer.AddMenuElement(PartsMenu,label='Duplicate Part',accelerator='Ctrl+C',underline=0)
        self.RotatePartDoer.AddMenuElement(PartsMenu,label='Rotate Part',underline=0)
        self.FlipPartHorizontallyDoer.AddMenuElement(PartsMenu,label='Flip Horizontally',underline=5)
        self.FlipPartVerticallyDoer.AddMenuElement(PartsMenu,label='Flip Vertically',underline=5)
        # ------
        WireMenu=Menu(self)
        TheMenu.add_cascade(label='Wires',menu=WireMenu,underline=0)
        self.AddWireDoer.AddMenuElement(WireMenu,label='Add Wire',underline=0)
        WireMenu.add_separator()
        self.DeleteVertexDoer.AddMenuElement(WireMenu,label='Delete Vertex',underline=7)
        self.DuplicateVertexDoer.AddMenuElement(WireMenu,label='Duplicate Vertex',underline=1)
        self.DeleteWireDoer.AddMenuElement(WireMenu,label='Delete Wire',underline=0)
        # ------
        ViewMenu=Menu(self)
        TheMenu.add_cascade(label='View',menu=ViewMenu,underline=0)
        self.ZoomInDoer.AddMenuElement(ViewMenu,label='Zoom In',underline=5)
        self.ZoomOutDoer.AddMenuElement(ViewMenu,label='Zoom Out',underline=5)
        self.PanDoer.AddMenuElement(ViewMenu,label='Pan',underline=0)
        # ------
        CalcMenu=Menu(self)
        TheMenu.add_cascade(label='Calculate',menu=CalcMenu,underline=0)
        self.CalculationPropertiesDoer.AddMenuElement(CalcMenu,label='Calculation Properties',underline=12)
        self.SParameterViewerDoer.AddMenuElement(CalcMenu,label='S-parameter Viewer',underline=12)
        CalcMenu.add_separator()
        self.CalculateSParametersDoer.AddMenuElement(CalcMenu,label='Calculate S-parameters',underline=0)
        self.SimulateDoer.AddMenuElement(CalcMenu,label='Simulate',underline=0)
        self.VirtualProbeDoer.AddMenuElement(CalcMenu,label='Virtual Probe',underline=9)
        self.DeembedDoer.AddMenuElement(CalcMenu,label='Deembed',underline=0)
        # ------
        HelpMenu=Menu(self)
        TheMenu.add_cascade(label='Help',menu=HelpMenu,underline=0)
        self.HelpDoer.AddMenuElement(HelpMenu,label='Help',underline=0)
        self.ControlHelpDoer.AddMenuElement(HelpMenu,label='Control Help',underline=0)

        # The Toolbar
        ToolBarFrame = Frame(self)
        ToolBarFrame.pack(side=TOP,fill=X,expand=NO)
        self.ClearProjectDoer.AddToolBarElement(ToolBarFrame,iconfile='./icons/png/16x16/actions/document-new-3.gif').Pack(side=LEFT,fill=NONE,expand=NO)
        self.OpenProjectDoer.AddToolBarElement(ToolBarFrame,iconfile='./icons/png/16x16/actions/document-open-2.gif',).Pack(side=LEFT,fill=NONE,expand=NO)
        self.SaveProjectDoer.AddToolBarElement(ToolBarFrame,iconfile='./icons/png/16x16/actions/document-save-2.gif').Pack(side=LEFT,fill=NONE,expand=NO)
        Frame(ToolBarFrame,bd=2,relief=SUNKEN).pack(side=LEFT,fill=X,padx=5,pady=5)
        self.AddPartDoer.AddToolBarElement(ToolBarFrame,iconfile='./icons/png/16x16/actions/edit-add-2.gif').Pack(side=LEFT,fill=NONE,expand=NO)
        self.DeleteSelectedDoer.AddToolBarElement(ToolBarFrame,iconfile='./icons/png/16x16/actions/edit-delete-6.gif').Pack(side=LEFT,fill=NONE,expand=NO)
        self.AddWireDoer.AddToolBarElement(ToolBarFrame,iconfile='./icons/png/16x16/actions/draw-line-3.gif').Pack(side=LEFT,fill=NONE,expand=NO)
        self.DuplicateSelectedDoer.AddToolBarElement(ToolBarFrame,iconfile='./icons/png/16x16/actions/edit-copy-3.gif').Pack(side=LEFT,fill=NONE,expand=NO)
        self.RotatePartDoer.AddToolBarElement(ToolBarFrame,iconfile='./icons/png/16x16/actions/object-rotate-left-4.gif').Pack(side=LEFT,fill=NONE,expand=NO)
        self.FlipPartHorizontallyDoer.AddToolBarElement(ToolBarFrame,iconfile='./icons/png/16x16/actions/object-flip-horizontal-3.gif').Pack(side=LEFT,fill=NONE,expand=NO)
        self.FlipPartVerticallyDoer.AddToolBarElement(ToolBarFrame,iconfile='./icons/png/16x16/actions/object-flip-vertical-3.gif').Pack(side=LEFT,fill=NONE,expand=NO)
        Frame(ToolBarFrame,height=2,bd=2,relief=RAISED).pack(side=LEFT,fill=X,padx=5,pady=5)
        self.ZoomInDoer.AddToolBarElement(ToolBarFrame,iconfile='./icons/png/16x16/actions/zoom-in-3.gif').Pack(side=LEFT,fill=NONE,expand=NO)
        self.ZoomOutDoer.AddToolBarElement(ToolBarFrame,iconfile='./icons/png/16x16/actions/zoom-out-3.gif').Pack(side=LEFT,fill=NONE,expand=NO)
        self.PanDoer.AddToolBarElement(ToolBarFrame,iconfile='./icons/png/16x16/actions/edit-move.gif').Pack(side=LEFT,fill=NONE,expand=NO)
        Frame(ToolBarFrame,height=2,bd=2,relief=RAISED).pack(side=LEFT,fill=X,padx=5,pady=5)
        self.CalculationPropertiesDoer.AddToolBarElement(ToolBarFrame,iconfile='./icons/png/16x16/actions/tooloptions.gif').Pack(side=LEFT,fill=NONE,expand=NO)
        self.CalculateDoer.AddToolBarElement(ToolBarFrame,iconfile='./icons/png/16x16/actions/system-run-3.gif').Pack(side=LEFT,fill=NONE,expand=NO)
        # ------
        UndoFrame=Frame(ToolBarFrame)
        UndoFrame.pack(side=RIGHT,fill=NONE,expand=NO,anchor=E)
        self.UndoDoer.AddToolBarElement(UndoFrame,iconfile='./icons/png/16x16/actions/edit-undo-3.gif').Pack(side=LEFT,fill=NONE,expand=NO,anchor=E)
        self.RedoDoer.AddToolBarElement(UndoFrame,iconfile='./icons/png/16x16/actions/edit-redo-3.gif').Pack(side=LEFT,fill=NONE,expand=NO,anchor=E)

        # The Drawing (which contains the schecmatic)
        self.Drawing=Drawing(self)
        self.Drawing.pack(side=TOP,fill=BOTH,expand=YES)

        self.statusbar.pack(side=BOTTOM,fill=X,expand=NO)
        self.root.bind('<Key>',self.onKey)

        # The Simulator Dialog
        self.simulator = Simulator(self)
        self.calculationProperties=CalculationProperties(self)
        self.filename=None

        # The edit history (for undo)
        self.history=History(self)

        self.root.mainloop()

    def onKey(self,event):
#       print "pressed", repr(event.keycode), repr(event.keysym)
        if event.keysym == 'Delete': # delete
            self.Drawing.DeleteSelected()

    def onUndo(self):
        self.history.Undo()
        self.Drawing.DrawSchematic()

    def onRedo(self):
        self.history.Redo()
        self.Drawing.DrawSchematic()

    def onReadProjectFromFile(self):
        self.Drawing.stateMachine.Nothing()
        extension='.xml'
        filename=askopenfilename(filetypes=[('xml', extension)])
        if filename == '':
            return
        filenametokens=filename.split('.')
        if len(filenametokens)==0:
            return
        if len(filenametokens)==1:
            filename=filename+extension
        filename=ConvertFileNameToRelativePath(filename)
        tree=et.parse(filename)
        root=tree.getroot()
        for child in root:
            if child.tag == 'drawing':
                self.Drawing.InitFromXml(child)
            elif child.tag == 'calculation_properties':
                self.calculationProperties.InitFromXml(child, self)
        self.filename=filename
        self.Drawing.DrawSchematic()
        self.history.Event('read project')

    def onWriteProjectToFile(self):
        self.Drawing.stateMachine.Nothing()
        extension='.xml'
        if self.filename == None:
            filename=asksaveasfilename(filetypes=[('xml', extension)],defaultextension='.xml',initialdir=os.getcwd())
        else:
            filename=asksaveasfilename(filetypes=[('xml', extension)],defaultextension='.xml',initialfile=self.filename)
        if filename=='':
            return
        self.filename=filename
        projectElement=et.Element('Project')
        drawingElement=self.Drawing.xml()
        calculationPropertiesElement=self.calculationProperties.xml()
        projectElement.extend([drawingElement,calculationPropertiesElement])
        et.ElementTree(projectElement).write(filename)

    def onClearSchematic(self):
        self.Drawing.stateMachine.Nothing()
        self.Drawing.schematic.Clear()
        self.history.Event('new project')
        self.Drawing.DrawSchematic()
        self.filename=None

    def onExportNetlist(self):
        self.Drawing.stateMachine.Nothing()
        nld = NetListDialog(self,self.Drawing.schematic.NetList().Text())

    def onExportTpX(self):
        from TpX import TpX
        from TikZ import TikZ
        self.Drawing.stateMachine.Nothing()
        extension='.TpX'
        if self.filename == None:
            filename=asksaveasfilename(filetypes=[('tpx', extension)],defaultextension='.TpX',initialdir=os.getcwd())
        else:
            filename=asksaveasfilename(filetypes=[('tpx', extension)],defaultextension='.TpX',initialfile=self.filename.replace('.xml','.TpX'))
        if filename=='':
            return
        try:
            tpx=self.Drawing.DrawSchematic(TpX()).Finish()
            tikz=self.Drawing.DrawSchematic(TikZ()).Finish()
            #tikz.Document()
            tpx.lineList=tpx.lineList+tikz.lineList
            tpx.WriteToFile(filename)
        except:
            tkMessageBox.showerror('Export LaTeX','LaTeX could not be generated or written ')

    def onAddPart(self):
        self.onAddPartFromSpecificList(DeviceList)

    def onAddUnknown(self):
        self.onAddPartFromSpecificList(DeviceListUnknown)

    def onAddSystem(self):
        self.onAddPartFromSpecificList(DeviceListSystem)

    def onAddPartFromSpecificList(self,deviceList):
        self.Drawing.stateMachine.Nothing()
        dpd=DevicePickerDialog(self,deviceList)
        if dpd.result != None:
            devicePicked=copy.deepcopy(deviceList[dpd.result])
            devicePicked.AddPartProperty(PartPropertyReferenceDesignator(''))
            defaultProperty = devicePicked[PartPropertyDefaultReferenceDesignator().propertyName]
            if defaultProperty != None:
                defaultPropertyValue = defaultProperty.GetValue()
                uniqueReferenceDesignator = self.Drawing.schematic.NewUniqueReferenceDesignator(defaultPropertyValue)
                if uniqueReferenceDesignator != None:
                    devicePicked[PartPropertyReferenceDesignator().propertyName].SetValueFromString(uniqueReferenceDesignator)
            dpe=DevicePropertiesDialog(self,devicePicked)
            if dpe.result != None:
                self.Drawing.partLoaded = dpe.result
                self.Drawing.stateMachine.PartLoaded()

    def onDeletePart(self):
        self.Drawing.DeleteSelectedDevice()
    def onDeleteSelected(self):
        self.Drawing.DeleteSelected()
    def onEditProperties(self):
        self.Drawing.EditSelectedDevice()
    def onRotatePart(self):
        if self.Drawing.stateMachine.state == 'DeviceSelected':
            self.Drawing.deviceSelected.partPicture.current.Rotate()
            self.Drawing.DrawSchematic()
    def onFlipPartHorizontally(self):
        if self.Drawing.stateMachine.state == 'DeviceSelected':
            orientation = self.Drawing.deviceSelected.partPicture.current.orientation
            mirroredHorizontally = self.Drawing.deviceSelected.partPicture.current.mirroredHorizontally
            mirroredVertically = self.Drawing.deviceSelected.partPicture.current.mirroredVertically
            self.Drawing.deviceSelected.partPicture.current.ApplyOrientation(orientation,not mirroredHorizontally,mirroredVertically)
            self.Drawing.DrawSchematic()
    def onFlipPartVertically(self):
        if self.Drawing.stateMachine.state == 'DeviceSelected':
            orientation = self.Drawing.deviceSelected.partPicture.current.orientation
            mirroredHorizontally = self.Drawing.deviceSelected.partPicture.current.mirroredHorizontally
            mirroredVertically = self.Drawing.deviceSelected.partPicture.current.mirroredVertically
            self.Drawing.deviceSelected.partPicture.current.ApplyOrientation(orientation,mirroredHorizontally,not mirroredVertically)
            self.Drawing.DrawSchematic()
    def onDuplicateSelected(self):
        self.Drawing.DuplicateSelected()
    def onCutMultipleSelections(self):
        self.Drawing.CutMultipleSelections()
    def onDuplicate(self):
        self.Drawing.DuplicateSelectedDevice()
    def onAddWire(self):
        self.Drawing.wireLoaded=Wire([Vertex((0,0))])
        self.Drawing.schematic.wireList.append(self.Drawing.wireLoaded)
        self.Drawing.stateMachine.WireLoaded()
    def onAddPort(self):
        self.Drawing.stateMachine.Nothing()
        portNumber=1
        for device in self.Drawing.schematic.deviceList:
            if device['type'].GetValue() == 'Port':
                if portNumber <= int(device['portnumber'].GetValue()):
                    portNumber = int(device['portnumber'].GetValue())+1
        dpe=DevicePropertiesDialog(self,Port(portNumber))
        if dpe.result != None:
            self.Drawing.partLoaded = dpe.result
            self.Drawing.stateMachine.PartLoaded()

    def onAddOutputProbe(self):
        self.AddSpecificPart(DeviceOutput())

    def onAddMeasureProbe(self):
        self.AddSpecificPart(DeviceMeasurement())

    def onAddStim(self):
        self.AddSpecificPart(DeviceStim())

    def AddSpecificPart(self,part):
        self.Drawing.stateMachine.Nothing()
        devicePicked=part
        devicePicked.AddPartProperty(PartPropertyReferenceDesignator(''))
        defaultProperty = devicePicked[PartPropertyDefaultReferenceDesignator().propertyName]
        if defaultProperty != None:
            defaultPropertyValue = defaultProperty.GetValue()
            uniqueReferenceDesignator = self.Drawing.schematic.NewUniqueReferenceDesignator(defaultPropertyValue)
            if uniqueReferenceDesignator != None:
                devicePicked[PartPropertyReferenceDesignator().propertyName].SetValueFromString(uniqueReferenceDesignator)
        dpe=DevicePropertiesDialog(self,devicePicked)
        if dpe.result != None:
            self.Drawing.partLoaded = dpe.result
            self.Drawing.stateMachine.PartLoaded()

    def onZoomIn(self):
        self.Drawing.grid = self.Drawing.grid*2
        self.Drawing.DrawSchematic()

    def onZoomOut(self):
        self.Drawing.grid = max(1,self.Drawing.grid/2)
        self.Drawing.DrawSchematic()

    def onPan(self):
        self.Drawing.stateMachine.Panning()

    def onDeleteSelectedVertex(self):
        self.Drawing.DeleteSelectedVertex()

    def onDuplicateSelectedVertex(self):
        self.Drawing.DuplicateSelectedVertex()

    def onDeleteSelectedWire(self):
        self.Drawing.DeleteSelectedWire()

    def onCalculateSParameters(self):
        self.Drawing.stateMachine.Nothing()
        netList=self.Drawing.schematic.NetList().Text()
        import SignalIntegrity as si
        spnp=si.p.SystemSParametersNumericParser(
            si.fd.EvenlySpacedFrequencyList(
                self.calculationProperties.endFrequency,
                self.calculationProperties.frequencyPoints))
        spnp.AddLines(netList)
        try:
            sp=spnp.SParameters()
        except si.PySIException as e:
            if e == si.PySIExceptionCheckConnections:
                tkMessageBox.showerror('S-parameter Calculator','Unconnected devices error: '+e.message)
            elif e == si.PySIExceptionSParameterFile:
                tkMessageBox.showerror('S-parameter Calculator','s-parameter file error: '+e.message)
            elif e == si.PySIExceptionNumeric:
                tkMessageBox.showerror('S-parameter Calculator','S-parameter Calculator Numerical Error: '+e.message)
            elif e == si.PySIExceptionSystemDescriptionBuildError:
                tkMessageBox.showerror('S-parameter Calculator','Schematic Error: '+e.message)
            else:
                tkMessageBox.showerror('S-parameter Calculator','Unhandled PySI Exception: '+str(e)+' '+e.message)
            return
        if self.filename is None:
            filename = None
        else:
            filename=self.filename.split('.')
            filename='.'.join(filename[:-1])
        SParametersDialog(self,sp,filename=filename)

    def onCalculationProperties(self):
        self.Drawing.stateMachine.Nothing()
        self.calculationProperties.ShowCalculationPropertiesDialog()

    def onSimulate(self):
        self.Drawing.stateMachine.Nothing()
        self.simulator.Simulate()

    def onVirtualProbe(self):
        self.Drawing.stateMachine.Nothing()
        self.simulator.VirtualProbe()

    def onDeembed(self):
        self.Drawing.stateMachine.Nothing()
        netList=self.Drawing.schematic.NetList().Text()
        import SignalIntegrity as si
        dnp=si.p.DeembedderNumericParser(
            si.fd.EvenlySpacedFrequencyList(
                self.calculationProperties.endFrequency,
                self.calculationProperties.frequencyPoints))
        dnp.AddLines(netList)
        try:
            sp=dnp.Deembed()
        except si.PySIException as e:
            if e == si.PySIExceptionCheckConnections:
                tkMessageBox.showerror('S-parameter Calculator','Unconnected devices error: '+e.message)
            elif e == si.PySIExceptionSParameterFile:
                tkMessageBox.showerror('S-parameter Calculator','s-parameter file error: '+e.message)
            elif e == si.PySIExceptionNumeric:
                tkMessageBox.showerror('S-parameter Calculator','S-parameter Calculator Numerical Error: '+e.message)
            elif e == si.PySIExceptionSystemDescriptionBuildError:
                tkMessageBox.showerror('S-parameter Calculator','Schematic Error: '+e.message)
            else:
                tkMessageBox.showerror('S-parameter Calculator','Unhandled PySI Exception: '+str(e)+' '+e.message)
            return
        if self.filename is None:
            filename = None
        else:
            filename=self.filename.split('.')
            filename='.'.join(filename[:-1])
        SParametersDialog(self,sp,filename=filename)

    def onCalculate(self):
        self.Drawing.stateMachine.Nothing()
        self.Drawing.DrawSchematic()
        self.SimulateDoer.Execute()
        self.CalculateSParametersDoer.Execute()
        self.VirtualProbeDoer.Execute()
        self.DeembedDoer.Execute()

    def onSParameterViewer(self):
        import SignalIntegrity as si
        filetypes = [('s-parameter files', ('*.s*p'))]
        filename=askopenfilename(filetypes=filetypes,parent=self)
        if filename == '':
            return
        filenametokens=filename.split('.')
        if len(filenametokens)==0:
            return

        filename=ConvertFileNameToRelativePath(filename)
        sp=si.sp.File(filename)
        SParametersDialog(self,sp,filename)

    def onHelp(self):
        import webbrowser
        new = 0
        url = os.path.dirname(os.path.abspath(__file__))+'/Help/PySIHelp.xhtml'
        webbrowser.open(url,new=new)

    def onControlHelp(self):
        Doer.inHelp = not Doer.inHelp
        if Doer.inHelp:
            self.OpenProjectDoer.Activate(True)
            self.SaveProjectDoer.Activate(True)
            self.ClearProjectDoer.Activate(True)
            self.ExportNetListDoer.Activate(True)
            self.ExportTpXDoer.Activate(True)
            # ------
            self.UndoDoer.Activate(True)
            self.RedoDoer.Activate(True)
            # ------
            self.AddPartDoer.Activate(True)
            self.AddPortDoer.Activate(True)
            self.AddMeasureProbeDoer.Activate(True)
            self.AddOutputProbeDoer.Activate(True)
            self.AddStimDoer.Activate(True)
            self.AddUnknownDoer.Activate(True)
            self.AddSystemDoer.Activate(True)
            self.DeletePartDoer.Activate(True)
            self.DeleteSelectedDoer.Activate(True)
            self.EditPropertiesDoer.Activate(True)
            self.DuplicatePartDoer.Activate(True)
            self.DuplicateSelectedDoer.Activate(True)
            self.CutSelectedDoer.Activate(True)
            self.RotatePartDoer.Activate(True)
            self.FlipPartHorizontallyDoer.Activate(True)
            self.FlipPartVerticallyDoer.Activate(True)
            # ------
            self.AddWireDoer.Activate(True)
            self.DeleteVertexDoer.Activate(True)
            self.DuplicateVertexDoer.Activate(True)
            self.DeleteWireDoer.Activate(True)
            # ------
            self.ZoomInDoer.Activate(True)
            self.ZoomOutDoer.Activate(True)
            self.PanDoer.Activate(True)
            # ------
            self.CalculationPropertiesDoer.Activate(True)
            self.SParameterViewerDoer.Activate(True)
            self.CalculateDoer.Activate(True)
            self.CalculateSParametersDoer.Activate(True)
            self.VirtualProbeDoer.Activate(True)
            self.SimulateDoer.Activate(True)
            self.DeembedDoer.Activate(True)
            # ------
            self.HelpDoer.Activate(True)
            self.ControlHelpDoer.Activate(True)
            # ------
            self.EscapeDoer.Activate(True)

            self.config(cursor='question_arrow')

    def onEscape(self):
        self.Drawing.stateMachine.Nothing(True)
        Doer.inHelp = False
        self.config(cursor='left_ptr')

def main():
    app=TheApp()

if __name__ == '__main__':
    main()