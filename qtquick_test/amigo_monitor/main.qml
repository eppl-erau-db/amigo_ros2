import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: appWindow
    title: "AMIGO Monitor"
    visible: true
    width: 1100
    height: 920
    minimumWidth: 860
    minimumHeight: 700
    color: "#0f0f12"

    // ── Shared helpers ─────────────────────────────────────────────────────────
    function statusColor(status) {
        if (status === "online")  return "#00ff66"
        if (status === "idle")    return "#ffaa00"
        return "#ff3333"
    }

    function statusBgColor(status) {
        if (status === "online")  return "#0a2218"
        if (status === "idle")    return "#221800"
        return "#220a0a"
    }

    function statusBorderColor(status) {
        if (status === "online")  return "#00cc66"
        if (status === "idle")    return "#cc8800"
        return "#cc2222"
    }

    // ── Command status helpers ─────────────────────────────────────────────────
    function formatStatus(raw) {
        if (!raw) return "—"
        return raw.replace(/_/g, " ").replace(/\b\w/g, function(c) { return c.toUpperCase() })
    }

    function bringupColor(s) {
        if (s === "running")  return "#00cc66"
        if (s === "starting") return "#0088ff"
        if (s === "done")     return "#00cc66"
        if (s === "stopped")  return "#ffaa00"
        if (s === "failed")   return "#ff3333"
        return "#444450"
    }

    function searchColor(s) {
        if (s === "succeeded")              return "#00cc66"
        if (s === "stable_estimate_found")  return "#00ffaa"
        if (s === "leak_detected")          return "#ff6633"
        if (s === "localizing")             return "#cc88ff"
        if (s === "server unavailable")     return "#ff3333"
        if (s === "goal rejected")          return "#ff6633"
        if (s === "canceled")               return "#ffaa00"
        if (s === "failed")                 return "#ff3333"
        if (s === "send error")             return "#ff3333"
        if (s === "sending goal")           return "#0088ff"
        if (s === "idle")                   return "#444450"
        // Exploration stages → cyan
        return "#00ccff"
    }

    function searchPulsing(s) {
        return s !== "idle" && s !== "succeeded" && s !== "failed" &&
               s !== "canceled" && s !== "done"  && s !== "stopped" &&
               s !== "server unavailable" && s !== "goal rejected" &&
               s !== "send error"
    }

    // ── Root layout ────────────────────────────────────────────────────────────
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 16

        // ── Header ─────────────────────────────────────────────────────────────
        RowLayout {
            Layout.fillWidth: true
            spacing: 14

            // Accent bar
            Rectangle {
                width: 5
                height: 30
                radius: 2.5
                gradient: Gradient {
                    GradientStop { position: 0.0; color: "#00cc66" }
                    GradientStop { position: 1.0; color: "#0088ff" }
                }
            }

            Text {
                text: "AMIGO"
                font.bold: true
                font.pointSize: 20
                color: "#ffffff"
            }

            Rectangle {
                Layout.preferredWidth: 1
                Layout.preferredHeight: 24
                color: "#333338"
                Layout.leftMargin: 4
                Layout.rightMargin: 4
            }

            Text {
                text: "Inspection & Robot Health Dashboard"
                font.pointSize: 11
                color: "#555560"
            }

            Item { Layout.fillWidth: true }

            // Live clock
            Text {
                id: clockText
                font.pointSize: 11
                font.family: "monospace"
                color: "#444450"
            }

            Timer {
                interval: 1000
                running: true
                repeat: true
                triggeredOnStart: true
                onTriggered: clockText.text = Qt.formatDateTime(new Date(), "hh:mm:ss")
            }
        }

        // ── Divider ────────────────────────────────────────────────────────────
        Rectangle {
            Layout.fillWidth: true
            height: 1
            color: "#22222a"
        }

        // ── Two-panel main content ─────────────────────────────────────────────
        RowLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 16

            // ────────────────────────────────────────────────────────────────────
            // LEFT PANEL — Anomaly Monitor
            // ────────────────────────────────────────────────────────────────────
            Rectangle {
                Layout.preferredWidth: 370
                Layout.fillHeight: true
                radius: 14
                color: "#18181c"
                border.width: 1
                border.color: "#2e2e36"

                // Subtle top gradient tint
                Rectangle {
                    width: parent.width; height: 80
                    radius: parent.radius
                    gradient: Gradient {
                        GradientStop { position: 0.0; color: "#18ff663a" }
                        GradientStop { position: 1.0; color: "#00000000" }
                    }
                }

                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 24
                    spacing: 18

                    // Section header
                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 8

                        RowLayout {
                            spacing: 10
                            Text {
                                text: "⚠"
                                font.pointSize: 16
                                color: "#ff6633"
                            }
                            Text {
                                text: "Anomaly Monitor"
                                font.bold: true
                                font.pointSize: 17
                                color: "#ffffff"
                            }
                        }
                        Rectangle {
                            Layout.fillWidth: true
                            height: 3
                            radius: 1.5
                            gradient: Gradient {
                                orientation: Gradient.Horizontal
                                GradientStop { position: 0.0; color: "#ff6633" }
                                GradientStop { position: 0.5; color: "#ff3366" }
                                GradientStop { position: 1.0; color: "#00000000" }
                            }
                        }
                    }

                    // ── Big stat cards ──────────────────────────────────────────
                    RowLayout {
                        Layout.fillWidth: true
                        spacing: 12

                        // Detected
                        Rectangle {
                            Layout.fillWidth: true
                            height: 110
                            radius: 10
                            color: "#120600"
                            border.width: 1
                            border.color: "#993322"

                            ColumnLayout {
                                anchors.centerIn: parent
                                spacing: 4

                                Text {
                                    text: anomalyBridge.detected
                                    font.bold: true
                                    font.pointSize: 46
                                    color: "#ff6633"
                                    Layout.alignment: Qt.AlignHCenter

                                    Behavior on text {
                                        SequentialAnimation {
                                            NumberAnimation {
                                                target: detectedCountText
                                                property: "scale"
                                                from: 1.0; to: 1.2; duration: 100
                                            }
                                            NumberAnimation {
                                                target: detectedCountText
                                                property: "scale"
                                                from: 1.2; to: 1.0; duration: 100
                                            }
                                        }
                                    }
                                }
                                Text {
                                    text: "Detected"
                                    font.pointSize: 10
                                    font.bold: true
                                    color: "#884422"
                                    Layout.alignment: Qt.AlignHCenter
                                }
                            }
                        }

                        // Inspected
                        Rectangle {
                            Layout.fillWidth: true
                            height: 110
                            radius: 10
                            color: "#020f08"
                            border.width: 1
                            border.color: "#226644"

                            ColumnLayout {
                                anchors.centerIn: parent
                                spacing: 4

                                Text {
                                    text: anomalyBridge.inspected
                                    font.bold: true
                                    font.pointSize: 46
                                    color: "#00cc88"
                                    Layout.alignment: Qt.AlignHCenter
                                }
                                Text {
                                    text: "Inspected"
                                    font.pointSize: 10
                                    font.bold: true
                                    color: "#226644"
                                    Layout.alignment: Qt.AlignHCenter
                                }
                            }
                        }
                    }

                    // ── Progress bar ────────────────────────────────────────────
                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 7

                        RowLayout {
                            Layout.fillWidth: true
                            Text {
                                text: "Inspection Progress"
                                font.pointSize: 10
                                color: "#666670"
                            }
                            Item { Layout.fillWidth: true }
                            Text {
                                text: anomalyBridge.detected > 0
                                    ? Math.round(anomalyBridge.inspected / anomalyBridge.detected * 100) + "%"
                                    : "—"
                                font.pointSize: 11
                                font.bold: true
                                color: "#00cc88"
                            }
                        }

                        // Track
                        Rectangle {
                            Layout.fillWidth: true
                            height: 8
                            radius: 4
                            color: "#222228"

                            // Fill
                            Rectangle {
                                width: anomalyBridge.detected > 0
                                    ? Math.min(parent.width * (anomalyBridge.inspected / anomalyBridge.detected), parent.width)
                                    : 0
                                height: parent.height
                                radius: parent.radius
                                gradient: Gradient {
                                    orientation: Gradient.Horizontal
                                    GradientStop { position: 0.0; color: "#00aa66" }
                                    GradientStop { position: 1.0; color: "#00ffaa" }
                                }
                                Behavior on width { NumberAnimation { duration: 350; easing.type: Easing.OutCubic } }
                            }
                        }
                    }

                    // ── Status badge ────────────────────────────────────────────
                    Rectangle {
                        Layout.fillWidth: true
                        height: 52
                        radius: 10
                        color: (anomalyBridge.detected - anomalyBridge.inspected) > 0 ? "#1a0a00" : "#001a0d"
                        border.width: 1
                        border.color: (anomalyBridge.detected - anomalyBridge.inspected) > 0 ? "#884422" : "#226644"

                        Behavior on color     { ColorAnimation { duration: 250 } }
                        Behavior on border.color { ColorAnimation { duration: 250 } }

                        RowLayout {
                            anchors.centerIn: parent
                            spacing: 10

                            Text {
                                text: {
                                    var pending = anomalyBridge.detected - anomalyBridge.inspected
                                    if (anomalyBridge.detected === 0) return "○"
                                    return pending > 0 ? "⚠" : "✓"
                                }
                                font.pointSize: 18
                                color: {
                                    var pending = anomalyBridge.detected - anomalyBridge.inspected
                                    if (anomalyBridge.detected === 0) return "#444450"
                                    return pending > 0 ? "#ff6633" : "#00cc88"
                                }
                                Behavior on color { ColorAnimation { duration: 250 } }
                            }

                            Text {
                                text: {
                                    var pending = anomalyBridge.detected - anomalyBridge.inspected
                                    if (anomalyBridge.detected === 0) return "No anomalies recorded"
                                    if (pending > 0) return pending + (pending === 1 ? " anomaly" : " anomalies") + " pending inspection"
                                    return "All anomalies inspected"
                                }
                                font.pointSize: 12
                                font.bold: true
                                color: {
                                    var pending = anomalyBridge.detected - anomalyBridge.inspected
                                    if (anomalyBridge.detected === 0) return "#444450"
                                    return pending > 0 ? "#ff9966" : "#00ffaa"
                                }
                                Behavior on color { ColorAnimation { duration: 250 } }
                            }
                        }
                    }

                    Item { Layout.fillHeight: true }

                    // ── Action buttons ──────────────────────────────────────────
                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 10

                        // Log Anomaly
                        Rectangle {
                            Layout.fillWidth: true
                            height: 48
                            radius: 8
                            color: btnLog.containsMouse ? "#aa3311" : "#882200"
                            border.width: 1
                            border.color: "#ff5522"

                            Behavior on color { ColorAnimation { duration: 120 } }

                            RowLayout {
                                anchors.centerIn: parent
                                spacing: 8
                                Text { text: "+"; font.pointSize: 18; font.bold: true; color: "#ffffff" }
                                Text { text: "Log New Anomaly"; font.pointSize: 13; font.bold: true; color: "#ffffff" }
                            }

                            MouseArea {
                                id: btnLog
                                anchors.fill: parent
                                hoverEnabled: true
                                cursorShape: Qt.PointingHandCursor
                                onClicked: anomalyBridge.addDetected()
                            }
                        }

                        // Mark Inspected
                        Rectangle {
                            Layout.fillWidth: true
                            height: 48
                            radius: 8
                            color: btnInspect.containsMouse && canInspect ? "#006633" : "#004422"
                            border.width: 1
                            border.color: "#00cc66"
                            opacity: canInspect ? 1.0 : 0.35

                            property bool canInspect: anomalyBridge.inspected < anomalyBridge.detected

                            Behavior on color   { ColorAnimation { duration: 120 } }
                            Behavior on opacity { NumberAnimation { duration: 200 } }

                            RowLayout {
                                anchors.centerIn: parent
                                spacing: 8
                                Text { text: "✓"; font.pointSize: 16; font.bold: true; color: "#ffffff" }
                                Text { text: "Mark as Inspected"; font.pointSize: 13; font.bold: true; color: "#ffffff" }
                            }

                            MouseArea {
                                id: btnInspect
                                anchors.fill: parent
                                hoverEnabled: true
                                cursorShape: parent.canInspect ? Qt.PointingHandCursor : Qt.ArrowCursor
                                onClicked: anomalyBridge.addInspected()
                            }
                        }

                        // Reset
                        Rectangle {
                            Layout.fillWidth: true
                            height: 36
                            radius: 8
                            color: btnReset.containsMouse ? "#1e1e24" : "transparent"
                            border.width: 1
                            border.color: "#33333a"

                            Behavior on color { ColorAnimation { duration: 120 } }

                            Text {
                                anchors.centerIn: parent
                                text: "Reset Counters"
                                font.pointSize: 10
                                color: "#555560"
                            }

                            MouseArea {
                                id: btnReset
                                anchors.fill: parent
                                hoverEnabled: true
                                cursorShape: Qt.PointingHandCursor
                                onClicked: anomalyBridge.reset()
                            }
                        }
                    }
                }
            }

            // ────────────────────────────────────────────────────────────────────
            // RIGHT PANEL — Robot Health
            // ────────────────────────────────────────────────────────────────────
            Rectangle {
                Layout.fillWidth: true
                Layout.fillHeight: true
                radius: 14
                color: "#18181c"
                border.width: 1
                border.color: "#2e2e36"

                // Subtle top gradient tint
                Rectangle {
                    width: parent.width; height: 80
                    radius: parent.radius
                    gradient: Gradient {
                        GradientStop { position: 0.0; color: "#120088ff" }
                        GradientStop { position: 1.0; color: "#00000000" }
                    }
                }

                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 24
                    spacing: 18

                    // Section header
                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 8

                        RowLayout {
                            spacing: 10
                            Text {
                                text: "◈"
                                font.pointSize: 14
                                color: "#0099ff"
                            }
                            Text {
                                text: "Robot Health"
                                font.bold: true
                                font.pointSize: 17
                                color: "#ffffff"
                            }
                        }
                        Rectangle {
                            Layout.fillWidth: true
                            height: 3
                            radius: 1.5
                            gradient: Gradient {
                                orientation: Gradient.Horizontal
                                GradientStop { position: 0.0; color: "#0088ff" }
                                GradientStop { position: 0.5; color: "#00ccff" }
                                GradientStop { position: 1.0; color: "#00000000" }
                            }
                        }
                    }

                    // ── Summary strip ───────────────────────────────────────────
                    RowLayout {
                        Layout.fillWidth: true
                        spacing: 10

                        // Online pill
                        Rectangle {
                            height: 32
                            width: summaryOnline.width + 28
                            radius: 16
                            color: "#0a2218"
                            border.width: 1
                            border.color: "#226644"

                            RowLayout {
                                id: summaryOnline
                                anchors.centerIn: parent
                                spacing: 6

                                Rectangle {
                                    width: 8; height: 8; radius: 4
                                    color: "#00ff66"

                                    SequentialAnimation on opacity {
                                        running: healthModel.onlineCount > 0
                                        loops: Animation.Infinite
                                        NumberAnimation { from: 1.0; to: 0.2; duration: 900 }
                                        NumberAnimation { from: 0.2; to: 1.0; duration: 900 }
                                    }
                                }

                                Text {
                                    text: healthModel.onlineCount + " Online"
                                    font.pointSize: 10
                                    font.bold: true
                                    color: "#00cc66"
                                }
                            }
                        }

                        // Idle pill
                        Rectangle {
                            height: 32
                            width: summaryIdle.width + 28
                            radius: 16
                            color: "#160e00"
                            border.width: 1
                            border.color: "#664400"

                            RowLayout {
                                id: summaryIdle
                                anchors.centerIn: parent
                                spacing: 6

                                Rectangle { width: 8; height: 8; radius: 4; color: "#ffaa00" }

                                Text {
                                    text: healthModel.idleCount + " Idle"
                                    font.pointSize: 10
                                    font.bold: true
                                    color: "#ffaa00"
                                }
                            }
                        }

                        // Offline pill
                        Rectangle {
                            height: 32
                            width: summaryOffline.width + 28
                            radius: 16
                            color: "#160202"
                            border.width: 1
                            border.color: "#661111"

                            RowLayout {
                                id: summaryOffline
                                anchors.centerIn: parent
                                spacing: 6

                                Rectangle { width: 8; height: 8; radius: 4; color: "#ff3333" }

                                Text {
                                    text: healthModel.offlineCount + " Offline"
                                    font.pointSize: 10
                                    font.bold: true
                                    color: "#ff4444"
                                }
                            }
                        }

                        Item { Layout.fillWidth: true }

                        Text {
                            text: "Refreshes every 1s"
                            font.pointSize: 9
                            color: "#333338"
                        }
                    }

                    // ── Topic cards ─────────────────────────────────────────────
                    GridView {
                        id: healthGrid
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        model: healthModel
                        clip: true

                        // Two equal columns; height per row adapts to available space
                        cellWidth:  Math.floor(width / 2)
                        cellHeight: Math.min(Math.floor((height - 4) / 4), 130)

                        delegate: Item {
                            width:  healthGrid.cellWidth
                            height: healthGrid.cellHeight

                            Rectangle {
                                anchors.fill: parent
                                anchors.margins: 5
                                radius: 12
                                color: statusBgColor(model.status)
                                border.width: 2
                                border.color: statusBorderColor(model.status)

                                Behavior on border.color { ColorAnimation { duration: 400 } }
                                Behavior on color        { ColorAnimation { duration: 400 } }

                                // Subtle scan line for online topics
                                Rectangle {
                                    visible: model.status === "online"
                                    anchors.left: parent.left
                                    anchors.right: parent.right
                                    height: 1
                                    color: statusColor(model.status)
                                    opacity: 0.15
                                    anchors.top: parent.top
                                    anchors.topMargin: parent.height * 0.35
                                }

                                ColumnLayout {
                                    anchors.fill: parent
                                    anchors.margins: 14
                                    spacing: 3

                                    // Friendly alias
                                    Text {
                                        text: model.alias
                                        font.bold: true
                                        font.pointSize: 13
                                        color: "#e8e8ee"
                                        Layout.fillWidth: true
                                        elide: Text.ElideRight
                                    }

                                    // Raw topic name
                                    Text {
                                        text: model.topic
                                        font.pointSize: 9
                                        color: "#3a3a44"
                                        font.family: "monospace"
                                        Layout.fillWidth: true
                                        elide: Text.ElideRight
                                    }

                                    Item { Layout.fillHeight: true }

                                    // Status row
                                    RowLayout {
                                        Layout.fillWidth: true
                                        spacing: 6

                                        // LED dot
                                        Rectangle {
                                            width: 9; height: 9; radius: 4.5
                                            color: statusColor(model.status)

                                            SequentialAnimation on opacity {
                                                running: model.status === "online"
                                                loops: Animation.Infinite
                                                NumberAnimation { from: 1.0; to: 0.15; duration: 900 }
                                                NumberAnimation { from: 0.15; to: 1.0; duration: 900 }
                                            }
                                        }

                                        // Status label
                                        Text {
                                            text: model.status.toUpperCase()
                                            font.pointSize: 10
                                            font.bold: true
                                            color: statusColor(model.status)

                                            Behavior on color { ColorAnimation { duration: 400 } }
                                        }
                                    }
                                }
                            }
                        }
                    }

                    // ── Legend ──────────────────────────────────────────────────
                    RowLayout {
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignHCenter
                        spacing: 28

                        Repeater {
                            model: [
                                { label: "Online  — receiving data",   dot: "#00ff66" },
                                { label: "Idle  — no recent messages", dot: "#ffaa00" },
                                { label: "Offline  — topic not found", dot: "#ff3333" },
                            ]
                            delegate: RowLayout {
                                spacing: 6
                                Rectangle {
                                    width: 9; height: 9; radius: 4.5
                                    color: modelData.dot
                                    anchors.verticalCenter: parent.verticalCenter
                                }
                                Text {
                                    text: modelData.label
                                    font.pointSize: 9
                                    color: "#44444e"
                                    anchors.verticalCenter: parent.verticalCenter
                                }
                            }
                        }
                    }
                }
            }
        }

        // ── COMMAND BAR ───────────────────────────────────────────────────────
        Rectangle {
            Layout.fillWidth: true
            height: 148
            radius: 14
            color: "#18181c"
            border.width: 1
            border.color: "#2e2e36"

            // Subtle purple/magenta top tint for distinction
            Rectangle {
                width: parent.width; height: 60
                radius: parent.radius
                gradient: Gradient {
                    GradientStop { position: 0.0; color: "#10aa44ff" }
                    GradientStop { position: 1.0; color: "#00000000" }
                }
            }

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 18
                spacing: 12

                // Header
                RowLayout {
                    Layout.fillWidth: true
                    spacing: 10

                    Text { text: "⬡"; font.pointSize: 13; color: "#aa44ff" }
                    Text {
                        text: "Mission Control"
                        font.bold: true
                        font.pointSize: 15
                        color: "#ffffff"
                    }
                    Rectangle {
                        Layout.fillWidth: true
                        height: 1
                        color: "#2a2a32"
                        Layout.leftMargin: 4
                    }
                }

                // Three command slots
                RowLayout {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    spacing: 12

                    // ── SLOT 1: Bringup ───────────────────────────────────────
                    ColumnLayout {
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        spacing: 6

                        // Button
                        Rectangle {
                            Layout.fillWidth: true
                            height: 44
                            radius: 8
                            color: {
                                if (commandBridge.bringupStatus === "running") return "#003322"
                                if (commandBridge.bringupStatus === "starting") return "#001a33"
                                return btnBringupMouse.containsMouse ? "#1a1a2e" : "#111118"
                            }
                            border.width: 1
                            border.color: {
                                if (commandBridge.bringupStatus === "running")  return "#00cc66"
                                if (commandBridge.bringupStatus === "starting") return "#0088ff"
                                return "#333344"
                            }
                            opacity: (commandBridge.bringupStatus === "running" ||
                                      commandBridge.bringupStatus === "starting") ? 1.0 : 0.85

                            Behavior on color        { ColorAnimation { duration: 200 } }
                            Behavior on border.color { ColorAnimation { duration: 200 } }

                            RowLayout {
                                anchors.centerIn: parent
                                spacing: 8
                                Text {
                                    text: commandBridge.bringupStatus === "running"  ? "◼" :
                                          commandBridge.bringupStatus === "starting" ? "◌" : "▶"
                                    font.pointSize: 13
                                    color: bringupColor(commandBridge.bringupStatus)
                                }
                                Text {
                                    text: "Bringup"
                                    font.pointSize: 12
                                    font.bold: true
                                    color: "#e0e0e8"
                                }
                            }

                            MouseArea {
                                id: btnBringupMouse
                                anchors.fill: parent
                                hoverEnabled: true
                                cursorShape: Qt.PointingHandCursor
                                onClicked: commandBridge.startBringup()
                            }
                        }

                        // Status row
                        RowLayout {
                            Layout.fillWidth: true
                            spacing: 6

                            Rectangle {
                                width: 7; height: 7; radius: 3.5
                                color: bringupColor(commandBridge.bringupStatus)

                                SequentialAnimation on opacity {
                                    running: commandBridge.bringupStatus === "running" ||
                                             commandBridge.bringupStatus === "starting"
                                    loops: Animation.Infinite
                                    NumberAnimation { from: 1.0; to: 0.1; duration: 700 }
                                    NumberAnimation { from: 0.1; to: 1.0; duration: 700 }
                                }
                            }

                            Text {
                                text: formatStatus(commandBridge.bringupStatus)
                                font.pointSize: 9
                                color: bringupColor(commandBridge.bringupStatus)
                                font.family: "monospace"
                            }

                            Item { Layout.fillWidth: true }

                            Text {
                                text: "mapping.launch.py"
                                font.pointSize: 8
                                color: "#2a2a38"
                                font.family: "monospace"
                            }
                        }
                    }

                    // Divider
                    Rectangle { width: 1; Layout.fillHeight: true; color: "#252530" }

                    // ── SLOT 2: Explore & Inspect ─────────────────────────────
                    ColumnLayout {
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        spacing: 6

                        // Button
                        Rectangle {
                            Layout.fillWidth: true
                            height: 44
                            radius: 8
                            color: {
                                if (commandBridge.searchActive) return "#0a001a"
                                return btnExploreMouse.containsMouse ? "#1a1428" : "#111118"
                            }
                            border.width: 1
                            border.color: {
                                if (commandBridge.searchActive)
                                    return searchColor(commandBridge.searchStatus)
                                return "#333344"
                            }
                            opacity: commandBridge.searchActive ? 1.0 : 0.85

                            Behavior on border.color { ColorAnimation { duration: 300 } }
                            Behavior on color        { ColorAnimation { duration: 200 } }

                            RowLayout {
                                anchors.centerIn: parent
                                spacing: 8
                                Text {
                                    text: commandBridge.searchActive ? "◌" : "⬡"
                                    font.pointSize: 13
                                    color: commandBridge.searchActive
                                        ? searchColor(commandBridge.searchStatus)
                                        : "#aa44ff"

                                    SequentialAnimation on opacity {
                                        running: commandBridge.searchActive
                                        loops: Animation.Infinite
                                        NumberAnimation { from: 1.0; to: 0.2; duration: 600 }
                                        NumberAnimation { from: 0.2; to: 1.0; duration: 600 }
                                    }
                                }
                                Text {
                                    text: "Explore & Inspect"
                                    font.pointSize: 12
                                    font.bold: true
                                    color: commandBridge.searchActive ? "#ccbbee" : "#e0e0e8"
                                }
                            }

                            MouseArea {
                                id: btnExploreMouse
                                anchors.fill: parent
                                hoverEnabled: true
                                cursorShape: commandBridge.searchActive
                                    ? Qt.ArrowCursor : Qt.PointingHandCursor
                                enabled: !commandBridge.searchActive
                                onClicked: commandBridge.startExploreAndInspect()
                            }
                        }

                        // Status row
                        RowLayout {
                            Layout.fillWidth: true
                            spacing: 6

                            Rectangle {
                                width: 7; height: 7; radius: 3.5
                                color: searchColor(commandBridge.searchStatus)

                                SequentialAnimation on opacity {
                                    running: searchPulsing(commandBridge.searchStatus)
                                    loops: Animation.Infinite
                                    NumberAnimation { from: 1.0; to: 0.1; duration: 700 }
                                    NumberAnimation { from: 0.1; to: 1.0; duration: 700 }
                                }
                            }

                            Text {
                                text: formatStatus(commandBridge.searchStatus)
                                font.pointSize: 9
                                color: searchColor(commandBridge.searchStatus)
                                font.family: "monospace"
                                Layout.fillWidth: true
                                elide: Text.ElideRight
                            }

                            Text {
                                text: "Search action"
                                font.pointSize: 8
                                color: "#2a2a38"
                                font.family: "monospace"
                            }
                        }
                    }

                    // Divider
                    Rectangle { width: 1; Layout.fillHeight: true; color: "#252530" }

                    // ── SLOT 3: Emergency Stop ────────────────────────────────
                    ColumnLayout {
                        Layout.preferredWidth: 180
                        Layout.fillHeight: true
                        spacing: 6

                        // STOP button
                        Rectangle {
                            Layout.fillWidth: true
                            height: 44
                            radius: 8
                            color: btnStopMouse.containsMouse ? "#550000" : "#330000"
                            border.width: 2
                            border.color: "#cc0000"

                            Behavior on color { ColorAnimation { duration: 120 } }

                            // Pulsing danger border when something is active
                            Rectangle {
                                anchors.fill: parent
                                radius: parent.radius
                                color: "transparent"
                                border.width: 2
                                border.color: "#ff0000"
                                visible: commandBridge.bringupStatus === "running" ||
                                         commandBridge.searchActive

                                SequentialAnimation on opacity {
                                    running: parent.visible
                                    loops: Animation.Infinite
                                    NumberAnimation { from: 0.8; to: 0.0; duration: 600 }
                                    NumberAnimation { from: 0.0; to: 0.8; duration: 600 }
                                }
                            }

                            RowLayout {
                                anchors.centerIn: parent
                                spacing: 8
                                Text { text: "◼"; font.pointSize: 14; color: "#ff4444" }
                                Text {
                                    text: "STOP"
                                    font.pointSize: 14
                                    font.bold: true
                                    color: "#ffffff"
                                    font.letterSpacing: 2
                                }
                            }

                            MouseArea {
                                id: btnStopMouse
                                anchors.fill: parent
                                hoverEnabled: true
                                cursorShape: Qt.PointingHandCursor
                                onClicked: commandBridge.emergencyStop()
                            }
                        }

                        // Label
                        Text {
                            Layout.fillWidth: true
                            text: "Kills all navigation processes"
                            font.pointSize: 8
                            color: "#3a2222"
                            horizontalAlignment: Text.AlignHCenter
                        }
                    }
                }
            }
        }
    }
}
