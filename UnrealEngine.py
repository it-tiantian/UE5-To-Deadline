#!/usr/bin/env python3
from __future__ import absolute_import
from System import *
from System.Diagnostics import *
from System.IO import *

from Deadline.Plugins import DeadlinePlugin, PluginType
from Deadline.Scripting import *

def GetDeadlinePlugin():
    return UnrealEnginePlugin()

def CleanupDeadlinePlugin( deadlinePlugin ):
    deadlinePlugin.Cleanup()

class UnrealEnginePlugin( DeadlinePlugin ):
        
    def __init__( self ):
        self.InitializeProcessCallback += self.InitializeProcess
        self.RenderExecutableCallback += self.RenderExecutable
        self.RenderArgumentCallback += self.RenderArgument
        
    def Cleanup( self ):
        for stdoutHandler in self.StdoutHandlers:
            del stdoutHandler.HandleCallback
        
        del self.InitializeProcessCallback
        del self.RenderExecutableCallback
        del self.RenderArgumentCallback
    
    def InitializeProcess( self ):
        self.SingleFramesOnly = False
        self.PopupHandling = False
        
    def RenderExecutable( self ):
        version = self.GetIntegerPluginInfoEntryWithDefault( "Version", 5 ) 
        UEExeList = self.GetConfigEntry( "UE_" + str(version) + "_EditorExecutable" )
        UEExe = ""
        
        UEExe = FileUtils.SearchFileList( UEExeList )
        if( UEExe == "" ):
            self.FailRender( "Unreal Engine " + str(version) + " editor executable was not found in the semicolon separated list \"" + UEExeList + "\". The path to the editor executable can be configured from the Plugin Configuration in the Deadline Monitor." )
    
        return UEExe
        
    def RenderArgument( self ):
        arguments = []
    
        projectFile =  self.GetPluginInfoEntry( "ProjectFile" )
        projectFile = RepositoryUtils.CheckPathMapping( projectFile )
        arguments.append( '"{0}"'.format( projectFile ) )
        
        map = self.GetPluginInfoEntry( "Map" )
        arguments.append( '"{0}"'.format( map ) )
        arguments.append( '-game' )
        #arguments.append( '-MovieSceneCaptureType="/Script/MovieSceneCapture.AutomatedLevelSequenceCapture"' )
        
        levelSequence = self.GetPluginInfoEntry( "LevelSequence" )
        arguments.append( '-LevelSequence="{0}"'.format( levelSequence ) )

        SequenceConfig = self.GetPluginInfoEntry( "SequenceConfig" )
        arguments.append( '-MoviePipelineConfig="{0}"'.format( SequenceConfig ) )
        arguments.append( '-windowed' )
        arguments.append( '-Log' )
        arguments.append( '-StdOut' )
        arguments.append( '-allowStdOutLogVerbosity' )
        arguments.append( '-Unattended' )
           
        return " ".join( arguments )
'''
        version = self.GetIntegerPluginInfoEntryWithDefault( "Version", "5.0" ) 
        if version == "4" :
            arguments.append( '-NoLoadingScreen' )

            arguments.append( '-MovieStartFrame={0}'.format( self.GetStartFrame() ) )
            arguments.append( '-MovieEndFrame={0}'.format( self.GetEndFrame() ) )
        
            arguments.append( '-ForceRes' )
        
            if self.GetBooleanPluginInfoEntryWithDefault( "OverrideResolution", False ):
                xResolution = self.GetIntegerPluginInfoEntryWithDefault( "ResX", 1920 )
                yResolution = self.GetIntegerPluginInfoEntryWithDefault( "ResY", 1080 )        
                arguments.append( '-ResX={0}'.format( xResolution ) )
                arguments.append( '-ResY={0}'.format( yResolution ) )
                arguments.append( '-windowed' )

            if self.GetBooleanPluginInfoEntryWithDefault( "VSyncEnabled", False ):
                arguments.append( '-VSync' )
            else:
                arguments.append( '-NoVSync' )

            frameRate = self.GetIntegerPluginInfoEntryWithDefault( "FrameRate", 30 )
            arguments.append( '-MovieFrameRate={0}'.format( frameRate ) )
            
            if self.GetBooleanPluginInfoEntryWithDefault( "DisableTextureStreaming", False ):
                arguments.append( "-noTextureStreaming" )
            
            outputDir = self.GetPluginInfoEntryWithDefault( "OutputDir", "" )
            outputDir = RepositoryUtils.CheckPathMapping( outputDir )
            if outputDir != "":
                arguments.append( '-MovieFolder="{0}"'.format( outputDir ) )
                
            movieName = self.GetPluginInfoEntryWithDefault( "MovieName", "" )
            if movieName != "":
                arguments.append( '-MovieName="{0}"'.format( movieName ) )
            
            outputFormat = self.GetPluginInfoEntryWithDefault( "OutputFormat", "PNG" )
            arguments.append( '-MovieFormat={0}'.format( outputFormat ) )
            
            if outputFormat == "CustomRenderPasses":
                renderPasses = self.GetPluginInfoEntryWithDefault( "RenderPasses", "" )
                
                for renderPass in renderPasses:
                    arguments.append( '-CustomRenderPasses={0}'.format( renderPass ) )
                
                captureHDR = self.GetBooleanPluginInfoEntryWithDefault( "CaptureHDR", False )
                if captureHDR:
                    arguments.append( '-CaptureFramesInHDR')
                    
                    arguments.append( '-HDRCompressionQuality={0}'.format( self.GetIntegerPluginInfoEntryWithDefault( "HDRCompressionQuality", 0 ) ) )
                    
                    arguments.append( '-CaptureGamut={0}'.format( self.GetPluginInfoEntryWithDefault( "CaptureGamut", "HCGM_Rec709" ) ) )
            
            PPMaterial = self.GetPluginInfoEntryWithDefault( "PostProcessingMaterial", "" )
            if PPMaterial != "":
                arguments.append( '-PostProcessingMaterial="{0}"'.format( PPMaterial ) )
            
            movieQuality = self.GetIntegerPluginInfoEntryWithDefault( "OutputQuality", 75 )
            arguments.append( '-MovieQuality={0}'.format( movieQuality ) )
            
            cinematicMode = self.GetBooleanPluginInfoEntryWithDefault( "CinematicMode", True )
            if cinematicMode:
                arguments.append( '-MovieCinematicMode=Yes' )
            else:
                arguments.append( '-MovieCinematicMode=No' )
                
            warmup = self.GetIntegerPluginInfoEntryWithDefault( "WarmupFrames",0 )
            arguments.append( '-MovieWarmUpFrames={0}'.format(warmup) )
        else:
            SequenceConfig = self.GetPluginInfoEntry( "SequenceConfig" )
            arguments.append( '-SequenceConfig="{0}"'.format( SequenceConfig ) )
            arguments.append( '-windowed' )
            arguments.append( '-Log' )
            arguments.append( '-StdOut' )
            arguments.append( '-allowStdOutLogVerbosity' )
            arguments.append( '-Unattended' )
'''     