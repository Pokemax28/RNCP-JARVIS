// src/components/ui/calendar.js

import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import interactionPlugin from "@fullcalendar/interaction";
import { useState } from "react";

export function Calendar() {
  const [events, setEvents] = useState([
    {
      title: "Séance haut du corps 💪",
      date: "2025-08-08",
      extendedProps: {
        type: "Sport",
        contenu: "Pompes, tractions, épaules, abdos",
      },
    },
    {
      title: "Cardio 🏃",
      date: "2025-08-10",
      extendedProps: {
        type: "Sport",
        contenu: "Course 30min + gainage",
      },
    },
  ]);

  const handleEventClick = (clickInfo) => {
    alert(
      `📅 ${clickInfo.event.title}\n📋 Détails : ${clickInfo.event.extendedProps.contenu}`
    );
  };

  return (
    <div className="border rounded shadow p-4">
      <h2 className="text-xl font-bold mb-4 text-center">Mon calendrier sportif</h2>
      <FullCalendar
        plugins={[dayGridPlugin, interactionPlugin]}
        initialView="dayGridMonth"
        events={events}
        eventClick={handleEventClick}
        height="auto"
      />
    </div>
  );
}

Calendar.displayName = "Calendar";
