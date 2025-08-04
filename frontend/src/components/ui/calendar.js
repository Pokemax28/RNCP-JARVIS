export function Calendar() {
    const today = new Date().toLocaleDateString();
  
    return (
      <div className="border rounded p-4 text-center">
        <h2 className="text-xl font-bold mb-2">Calendar</h2>
        <p>{today}</p>
        <p className="text-gray-500">[Empty for now]</p>
      </div>
    );
  }

Calendar.displayName = "Calendar";
export function CalendarHeader({ date }) {
    return (
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold">{date}</h3>
        <button className="text-blue-500">Today</button>
      </div>
    );
}