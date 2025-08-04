import React from "react";

export function Switch({ checked, onCheckedChange }) {
  const toggle = () => {
    onCheckedChange(!checked);
  };

  return (
    <div
      onClick={toggle}
      className={`w-12 h-6 flex items-center bg-gray-300 rounded-full p-1 cursor-pointer ${
        checked ? "bg-blue-500" : ""
      }`}
    >
      <div
        className={`bg-white w-4 h-4 rounded-full shadow-md transform duration-300 ${
          checked ? "translate-x-6" : ""
        }`}
      ></div>
    </div>
  );
}
Switch.displayName = "Switch";