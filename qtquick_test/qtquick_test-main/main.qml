import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtPositioning
import QtLocation

ApplicationWindow {
    title: qsTr("SystemMonitor")
    menuBar: mainMenu
    visible: true
    width: 800
    height: 500

    id: appWindow

    RowLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 20

        // --- Left side: stylized control panel ---
        Rectangle {
            id: sidePanel
            Layout.preferredWidth: 240
            Layout.fillHeight: true
            radius: 12
            color: "#1a1a1d"
            border.width: 1
            border.color: "#3f3f44"

            // Subtle gradient overlay
            Rectangle {
                anchors.fill: parent
                radius: parent.radius
                gradient: Gradient {
                    GradientStop { position: 0.0; color: "#22ffffff" }
                    GradientStop { position: 1.0; color: "#00000000" }
                }
            }

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 20
                spacing: 16

                // Panel title with accent
                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: 8

                    Text {
                        text: "Display Options"
                        font.bold: true
                        font.pointSize: 16
                        color: "#ffffff"
                        Layout.alignment: Qt.AlignLeft
                    }

                    Rectangle {
                        Layout.fillWidth: true
                        height: 3
                        radius: 1.5
                        gradient: Gradient {
                            orientation: Gradient.Horizontal
                            GradientStop { position: 0.0; color: "#00cc66" }
                            GradientStop { position: 0.5; color: "#0088ff" }
                            GradientStop { position: 1.0; color: "#00000000" }
                        }
                    }
                }

                Item { height: 10 } // Spacer

                // Map Visual Checkbox
                StyledCheckBox {
                    id: mapvizCheck
                    text: "Map Visual"
                    iconSymbol: "🗺️"
                    checked: false
                    Layout.fillWidth: true
                }

                // Topic Monitor Checkbox
                StyledCheckBox {
                    id: topicsCheck
                    text: "Topic Monitor"
                    iconSymbol: "📊"
                    checked: true
                    Layout.fillWidth: true
                }

                // Path Planning Checkbox
                StyledCheckBox {
                    id: pathsCheck
                    text: "Path Planning"
                    iconSymbol: "🛣️"
                    checked: false
                    Layout.fillWidth: true
                }

                // Navigation Status Checkbox
                StyledCheckBox {
                    id: navCheck
                    text: "Navigation Status"
                    iconSymbol: "🧭"
                    checked: false
                    Layout.fillWidth: true
                }

                Item { Layout.fillHeight: true } // Push everything to top

                // Info section at bottom
                Rectangle {
                    Layout.fillWidth: true
                    height: 60
                    radius: 8
                    color: "#15151a"
                    border.width: 1
                    border.color: "#2a2a2f"

                    ColumnLayout {
                        anchors.fill: parent
                        anchors.margins: 10
                        spacing: 4

                        Text {
                            text: "AMIGO's System Monitor"
                            font.pointSize: 10
                            font.bold: true
                            color: "#00cc66"
                        }

                        Text {
                            text: "ROS2 Interface"
                            font.pointSize: 8
                            color: "#888888"
                        }
                    }
                }
            }
        }

        // --- Right side: display grid with battery ---
        ColumnLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 15

            GridLayout {
                id: displayArea
                Layout.fillWidth: true
                Layout.fillHeight: true
                columns: 2
                rowSpacing: 10
                columnSpacing: 10

            Rectangle {
                id: mapContainer
                objectName: "mapContainer"
                visible: mapvizCheck.checked
                color: "#024c1c"
                radius: 10
                Layout.fillWidth: true
                Layout.fillHeight: true

                Map {
                    id: map
                    anchors.fill: parent
                    plugin: Plugin { name: "osm" }
                    center: QtPositioning.coordinate(locationBridge.gpsLatitude, locationBridge.gpsLongitude)
                    zoomLevel: 17
                    
                    // GPS Location Marker (Robot's current position)
                    MapQuickItem {
                        id: gpsMarker
                        coordinate: QtPositioning.coordinate(locationBridge.gpsLatitude, locationBridge.gpsLongitude)
                        anchorPoint.x: robotIcon.width / 2
                        anchorPoint.y: robotIcon.height / 2
                        
                        sourceItem: Item {
                            id: robotIcon
                            width: 30
                            height: 30
                            transformOrigin: Item.Center
                            rotation: locationBridge.odomHeading

                            // Background circle
                            Rectangle {
                                anchors.fill: parent
                                radius: width/2
                                color: "#0066ff"
                                border.width: 3
                                border.color: "#ffffff"
                                smooth: true
                            }

                            // Arrow indicator (points up by default, rotation applied to parent)
                            Text {
                                anchors.centerIn: parent
                                text: "▲"
                                color: "#ffffff"
                                font.pointSize: 16
                                horizontalAlignment: Text.AlignHCenter
                                verticalAlignment: Text.AlignVCenter
                            }

                            // Pulsing animation on the whole icon
                            SequentialAnimation on scale {
                                loops: Animation.Infinite
                                NumberAnimation { from: 1.0; to: 1.15; duration: 1000; easing.type: Easing.InOutQuad }
                                NumberAnimation { from: 1.15; to: 1.0; duration: 1000; easing.type: Easing.InOutQuad }
                            }
                        }
                    }
                    
                    // Accuracy circle around GPS position
                    MapCircle {
                        center: QtPositioning.coordinate(locationBridge.gpsLatitude, locationBridge.gpsLongitude)
                        radius: 5.0
                        color: "#330066ff"
                        border.width: 2
                        border.color: "#0066ff"
                    }
                    
                    // Waypoints Marker (Target destination)
                    MapQuickItem {
                        id: waypointMarker
                        coordinate: QtPositioning.coordinate(locationBridge.waypointLatitude, locationBridge.waypointLongitude)
                        anchorPoint.x: waypointIcon.width / 2
                        anchorPoint.y: waypointIcon.height
                        
                        sourceItem: Column {
                            spacing: 0
                            
                            // Waypoint flag
                            Rectangle {
                                id: waypointIcon
                                width: 40
                                height: 30
                                color: "#ff3333"
                                border.width: 2
                                border.color: "#ffffff"
                                radius: 4
                                
                                Text {
                                    anchors.centerIn: parent
                                    text: "⚑"
                                    font.pointSize: 16
                                    color: "#ffffff"
                                }
                            }
                            
                            // Flag pole
                            Rectangle {
                                width: 3
                                height: 20
                                color: "#ffffff"
                                anchors.horizontalCenter: parent.horizontalCenter
                            }
                        }
                    }
                    
                    // Line connecting robot to waypoint
                    MapPolyline {
                        line.width: 3
                        line.color: "#ffaa00"
                        path: [
                            QtPositioning.coordinate(locationBridge.gpsLatitude, locationBridge.gpsLongitude),
                            QtPositioning.coordinate(locationBridge.waypointLatitude, locationBridge.waypointLongitude)
                        ]
                    }
                }
                
                // Legend overlay
                Rectangle {
                    anchors.top: parent.top
                    anchors.right: parent.right
                    anchors.margins: 10
                    width: 150
                    height: legendColumn.height + 20
                    color: "#cc000000"
                    radius: 8
                    
                    Column {
                        id: legendColumn
                        anchors.centerIn: parent
                        spacing: 8
                        
                        Row {
                            spacing: 10
                            Rectangle {
                                width: 20
                                height: 20
                                radius: 10
                                color: "#0066ff"
                                border.width: 2
                                border.color: "#ffffff"
                                anchors.verticalCenter: parent.verticalCenter
                            }
                            Text {
                                text: "Robot Position"
                                color: "#ffffff"
                                font.pointSize: 9
                                anchors.verticalCenter: parent.verticalCenter
                            }
                        }
                        
                        Row {
                            spacing: 10
                            Rectangle {
                                width: 20
                                height: 16
                                color: "#ff3333"
                                border.width: 2
                                border.color: "#ffffff"
                                radius: 2
                                anchors.verticalCenter: parent.verticalCenter
                            }
                            Text {
                                text: "Waypoint"
                                color: "#ffffff"
                                font.pointSize: 9
                                anchors.verticalCenter: parent.verticalCenter
                            }
                        }
                    }
                }
            }

            // Topic Monitor
            Rectangle {
                id: topicsContainer
                objectName: "topicsContainer"
                visible: topicsCheck.checked
                color: "#1e1e1e"
                radius: 10
                Layout.fillWidth: true
                Layout.fillHeight: true

                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 20
                    spacing: 15

                    Text {
                        text: "System Status Monitor"
                        font.bold: true
                        font.pointSize: 18
                        color: "#ffffff"
                        Layout.alignment: Qt.AlignHCenter
                    }

                    Rectangle {
                        Layout.fillWidth: true
                        height: 2
                        color: "#3d3d3d"
                    }

                    ListView {
                        id: topicListView
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        model: topicModel
                        spacing: 12
                        clip: true

                        delegate: Rectangle {
                            width: topicListView.width
                            height: 70
                            color: "#2a2a2a"
                            radius: 8
                            border.width: 2
                            border.color: {
                                if (model.status === "Receiving") return "#00cc66"
                                else if (model.status === "No Data") return "#ff9933"
                                else return "#cc0000"
                            }

                            RowLayout {
                                anchors.fill: parent
                                anchors.margins: 15
                                spacing: 15

                                Rectangle {
                                    width: 24
                                    height: 24
                                    radius: 12
                                    color: {
                                        if (model.status === "Receiving") return "#00ff66"
                                        else if (model.status === "No Data") return "#ffaa00"
                                        else return "#ff3333"
                                    }
                                    
                                    SequentialAnimation on opacity {
                                        running: model.status === "Receiving"
                                        loops: Animation.Infinite
                                        NumberAnimation { from: 1.0; to: 0.3; duration: 800 }
                                        NumberAnimation { from: 0.3; to: 1.0; duration: 800 }
                                    }
                                    
                                    Layout.alignment: Qt.AlignVCenter
                                }

                                ColumnLayout {
                                    Layout.fillWidth: true
                                    spacing: 4

                                    Text {
                                        text: model.alias
                                        font.pointSize: 14
                                        font.bold: true
                                        color: "#ffffff"
                                        Layout.fillWidth: true
                                        elide: Text.ElideRight
                                    }

                                    Text {
                                        text: model.topic
                                        font.pointSize: 10
                                        color: "#888888"
                                        font.family: "monospace"
                                        Layout.fillWidth: true
                                        elide: Text.ElideMiddle
                                    }
                                }

                                Rectangle {
                                    Layout.preferredWidth: 120
                                    height: 40
                                    radius: 6
                                    color: {
                                        if (model.status === "Receiving") return "#003322"
                                        else if (model.status === "No Data") return "#332200"
                                        else return "#330000"
                                    }

                                    Text {
                                        anchors.centerIn: parent
                                        text: model.status.toUpperCase()
                                        font.pointSize: 11
                                        font.bold: true
                                        color: {
                                            if (model.status === "Receiving") return "#00ff66"
                                            else if (model.status === "No Data") return "#ffaa00"
                                            else return "#ff6666"
                                        }
                                    }
                                }
                            }

                            MouseArea {
                                anchors.fill: parent
                                hoverEnabled: true
                                onEntered: parent.color = "#333333"
                                onExited: parent.color = "#2a2a2a"
                            }
                        }

                        ScrollBar.vertical: ScrollBar {
                            policy: ScrollBar.AsNeeded
                            width: 10
                            
                            contentItem: Rectangle {
                                radius: 5
                                color: "#555555"
                            }
                        }
                    }

                    Rectangle {
                        Layout.fillWidth: true
                        height: 1
                        color: "#3d3d3d"
                    }

                    RowLayout {
                        Layout.fillWidth: true
                        spacing: 20
                        Layout.alignment: Qt.AlignHCenter

                        RowLayout {
                            spacing: 8
                            Rectangle {
                                width: 16
                                height: 16
                                radius: 8
                                color: "#00ff66"
                            }
                            Text {
                                text: "Receiving Data"
                                font.pointSize: 9
                                color: "#aaaaaa"
                            }
                        }

                        RowLayout {
                            spacing: 8
                            Rectangle {
                                width: 16
                                height: 16
                                radius: 8
                                color: "#ffaa00"
                            }
                            Text {
                                text: "No Data"
                                font.pointSize: 9
                                color: "#aaaaaa"
                            }
                        }

                        RowLayout {
                            spacing: 8
                            Rectangle {
                                width: 16
                                height: 16
                                radius: 8
                                color: "#ff3333"
                            }
                            Text {
                                text: "Offline"
                                font.pointSize: 9
                                color: "#aaaaaa"
                            }
                        }
                    }
                }
            }

            Rectangle {
                id: pathsContainer
                objectName: "pathsContainer"
                visible: pathsCheck.checked
                color: "#87CEEB"
                radius: 10
                Layout.fillWidth: true
                Layout.fillHeight: true
            }

            Rectangle {
                id: navContainer
                objectName: "navContainer"
                visible: navCheck.checked
                color: "#FFD700"
                radius: 10
                Layout.fillWidth: true
                Layout.fillHeight: true
            }
        }

            // Battery Status Bar
            Rectangle {
                id: batteryContainer
                Layout.fillWidth: true
                Layout.preferredHeight: 80
                radius: 10
                color: "#1a1a1d"
                border.width: 1
                border.color: "#3f3f44"

                RowLayout {
                    anchors.fill: parent
                    anchors.margins: 15
                    spacing: 20

                    // Battery Icon
                    Rectangle {
                        Layout.preferredWidth: 80
                        Layout.preferredHeight: 50
                        color: "transparent"

                        // Battery body
                        Rectangle {
                            id: batteryBody
                            anchors.left: parent.left
                            anchors.verticalCenter: parent.verticalCenter
                            width: 60
                            height: 35
                            radius: 4
                            color: "#2a2a2a"
                            border.width: 3
                            border.color: "#00cc66"  // Will change based on battery level

                            // Battery fill level
                            Rectangle {
                                id: batteryFill
                                anchors.left: parent.left
                                anchors.top: parent.top
                                anchors.bottom: parent.bottom
                                anchors.margins: 3
                                width: parent.width * 0.85  // 85% charge level (placeholder)
                                radius: 2
                                color: "#00ff66"  // Will change based on battery level
                                
                                // Animated shine effect
                                Rectangle {
                                    anchors.left: parent.left
                                    anchors.top: parent.top
                                    anchors.bottom: parent.bottom
                                    width: parent.width * 0.3
                                    gradient: Gradient {
                                        orientation: Gradient.Horizontal
                                        GradientStop { position: 0.0; color: "#33ffffff" }
                                        GradientStop { position: 1.0; color: "#00ffffff" }
                                    }
                                }
                            }
                        }

                        // Battery terminal
                        Rectangle {
                            anchors.left: batteryBody.right
                            anchors.leftMargin: -1
                            anchors.verticalCenter: parent.verticalCenter
                            width: 6
                            height: 18
                            radius: 2
                            color: "#00cc66"  // Will change based on battery level
                        }

                        // Lightning bolt icon (when charging)
                        Text {
                            id: chargingIcon
                            anchors.centerIn: batteryBody
                            text: "⚡"
                            font.pointSize: 18
                            color: "#ffffff"
                            visible: false  // Set to true when charging
                        }
                    }

                    // Battery Info
                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 4

                        RowLayout {
                            spacing: 10

                            Text {
                                text: "Battery Level"
                                font.pointSize: 12
                                font.bold: true
                                color: "#ffffff"
                            }

                            Text {
                                id: batteryPercentage
                                text: "85%"  // Placeholder
                                font.pointSize: 14
                                font.bold: true
                                color: "#00ff66"  // Will change based on battery level
                            }
                        }

                        Text {
                            id: batteryStatus
                            text: "Discharging · 2h 34m remaining"  // Placeholder
                            font.pointSize: 9
                            color: "#888888"
                        }
                    }

                    // Battery voltage and current
                    ColumnLayout {
                        Layout.preferredWidth: 150
                        spacing: 6

                        RowLayout {
                            spacing: 8
                            Text {
                                text: "Voltage:"
                                font.pointSize: 9
                                color: "#888888"
                            }
                            Text {
                                id: batteryVoltage
                                text: "24.8 V"  // Placeholder
                                font.pointSize: 10
                                font.bold: true
                                color: "#00cc66"
                            }
                        }

                        RowLayout {
                            spacing: 8
                            Text {
                                text: "Current:"
                                font.pointSize: 9
                                color: "#888888"
                            }
                            Text {
                                id: batteryCurrent
                                text: "3.2 A"  // Placeholder
                                font.pointSize: 10
                                font.bold: true
                                color: "#00cc66"
                            }
                        }
                    }
                }
            }
        }

    // Custom Checkbox Component
        component StyledCheckBox: CheckBox {
            id: control
            property string iconSymbol: "📋"
            
            spacing: 12

            indicator: Rectangle {
                implicitWidth: 22
                implicitHeight: 22
                x: control.leftPadding
                y: parent.height / 2 - height / 2
                radius: 5
                border.width: 2
                border.color: control.checked ? "#00cc66" : "#555555"
                color: control.checked ? "#003318" : "#222222"
                
                Behavior on border.color { ColorAnimation { duration: 150 } }
                Behavior on color { ColorAnimation { duration: 150 } }

                Text {
                    anchors.centerIn: parent
                    visible: control.checked
                    text: "✓"
                    color: "#00ff88"
                    font.bold: true
                    font.pointSize: 12
                }
            }

            contentItem: RowLayout {
                spacing: 10
                
                Item { width: control.indicator.width + control.spacing }
                
                Text {
                    text: control.iconSymbol
                    font.pointSize: 16
                    color: control.checked ? "#00ff88" : "#888888"
                    Behavior on color { ColorAnimation { duration: 150 } }
                }
                
                Text {
                    text: control.text
                    color: control.checked ? "#ffffff" : "#bbbbbb"
                    font.pointSize: 12
                    Layout.fillWidth: true
                    Behavior on color { ColorAnimation { duration: 150 } }
                }
            }

            background: Rectangle {
                color: control.hovered ? "#252529" : "transparent"
                radius: 6
                Behavior on color { ColorAnimation { duration: 150 } }
            }
        }
    }
}