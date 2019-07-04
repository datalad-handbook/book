
****************
Diagram examples
****************

Sequence diagrams
=================

.. uml::
   :caption: simple

   actor Foo1
   boundary Foo2
   control Foo3
   entity Foo4
   database Foo5
   collections Foo6
   Foo1 -> Foo2 : To boundary
   Foo1 -> Foo3 : To control
   Foo1 -> Foo4 : To entity
   Foo1 -> Foo5 : To database
   Foo1 -> Foo6 : To collections


.. uml::
   :caption: crazy

   skinparam backgroundColor #EEEBDC
   skinparam handwritten true

   skinparam sequence {
   	ArrowColor DeepSkyBlue
   	ActorBorderColor DeepSkyBlue
   	LifeLineBorderColor blue
   	LifeLineBackgroundColor #A9DCDF
   	
   	ParticipantBorderColor DeepSkyBlue
   	ParticipantBackgroundColor DodgerBlue
   	ParticipantFontName Impact
   	ParticipantFontSize 17
   	ParticipantFontColor #A9DCDF
   	
   	ActorBackgroundColor aqua
   	ActorFontColor DeepSkyBlue
   	ActorFontSize 17
   	ActorFontName Aapex
   }

   actor User
   participant "First Class" as A
   participant "Second Class" as B
   participant "Last Class" as C

   User -> A: DoWork
   activate A

   A -> B: Create Request
   activate B

   B -> C: DoWork
   activate C
   C --> B: WorkDone
   destroy C

   B --> A: Request Created
   deactivate B

   A --> User: Done
   deactivate A


Use case diagrams
=================

.. uml::

   :Main Admin: as Admin
   (Use the application) as (Use)

   User -> (Start)
   User --> (Use)

   Admin ---> (Use)

   note right of Admin : This is an example.

   note right of (Use)
     A note can also
     be on several lines
   end note

   note "This note is connected\nto several objects." as N2
   (Start) .. N2
   N2 .. (Use)


Flow charts
===========

.. uml::

   start
   :ClickServlet.handleRequest();
   :new page;
   if (Page.onSecurityCheck) then (true)
     :Page.onInit();
     if (isForward?) then (no)
           :Process controls;
           if (continue processing?) then (no)
             stop
           endif

           if (isPost?) then (yes)
             :Page.onPost();
           else (no)
             :Page.onGet();
           endif
           :Page.onRender();
     endif
   else (false)
   endif

   if (do redirect?) then (yes)
     :redirect process;
   else
     if (do forward?) then (yes)
           :Forward request;
     else (no)
           :Render page template;
     endif
   endif

   stop


Component diagrams
==================

.. uml::

   package "Some Group" {
     HTTP - [First Component]
     [Another Component]
   }

   node "Other Groups" {
     FTP - [Second Component]
     [First Component] --> FTP
   } 

   cloud {
     [Example 1]
   }


   database "MySql" {
     folder "This is my folder" {
           [Folder 3]
     }
     frame "Foo" {
           [Frame 4]
     }
   }


   [Another Component] --> [Example 1]
   [Example 1] --> [Folder 3]
   [Folder 3] --> [Frame 4]


Timing diagrams
===============

.. uml::

   robust "Web Browser" as WB
   concise "Web User" as WU

   WB is Initializing
   WU is Absent

   @WB
   0 is idle
   +200 is Processing
   +100 is Waiting
   WB@0 <-> @50 : {50 ms lag}

   @WU
   0 is Waiting
   +500 is ok
   @200 <-> @+150 : {150 ms}


GUI sketches
============

.. uml::

   salt
   {
     Just plain text
     [This is my button]
     ()  Unchecked radio
     (X) Checked radio
     []  Unchecked box
     [X] Checked box
     "Enter text here   "
     ^This is a droplist^
   }


Gantt charts
============

.. uml::

   @startgantt
   [Prototype design] lasts 13 days and is colored in Lavender/LightBlue
   [Test prototype] lasts 9 days and is colored in Coral/Green and starts 3 days after [Prototype design]'s end
   [Write tests] lasts 5 days and ends at [Prototype design]'s end
   [Hire tests writers] lasts 6 days and ends at [Write tests]'s start
   [Init and write tests report] is colored in Coral/Green
   [Init and write tests report] starts 1 day before [Test prototype]'s start and ends at [Test prototype]'s end
   @endgantt


.. note::

   plantuml version might be too old for the following


Mindmaps
========

.. uml::

   @startmindmap
   caption figure 1
   title My super title

   * <&flag>Debian
   ** <&globe>Ubuntu
   *** Linux Mint
   *** Kubuntu
   *** Lubuntu
   *** KDE Neon
   ** <&graph>LMDE
   ** <&pulse>SolydXK
   ** <&people>SteamOS
   ** <&star>Raspbian with a very long name
   *** <s>Raspmbc</s> => OSMC
   *** <s>Raspyfi</s> => Volumio

   header
   My super header
   endheader

   center footer My super footer

   legend right
     Short
     legend
   endlegend
   @endmindmap


Break down charts
=================

.. uml::

   @startwbs
   * Business Process Modelling WBS
   ** Launch the project
   *** Complete Stakeholder Research
   *** Initial Implementation Plan
   ** Design phase
   *** Model of AsIs Processes Completed
   ****< Model of AsIs Processes Completed1
   ****> Model of AsIs Processes Completed2
   ***< Measure AsIs performance metrics
   ***< Identify Quick Wins
   @endwbs
