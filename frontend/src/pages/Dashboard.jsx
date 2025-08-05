import React, { useState } from 'react';
import EmailList from '../components/EmailList';

export default function Dashboard() {
  const [selectedFolder, setSelectedFolder] = useState('All');

  const folders = ['All', 'Phishing', 'Spam', 'À traiter'];

  return (
    <div className="flex h-screen">
      <aside className="w-64 bg-gray-800 text-white p-4">
        <h2 className="text-2xl font-bold mb-4">Folders</h2>
        <ul className="space-y-2">
          {folders.map(folder => (
            <li
              key={folder}
              className={`cursor-pointer ${selectedFolder === folder ? 'font-bold' : ''}`}
              onClick={() => setSelectedFolder(folder)}
            >
              {folder}
            </li>
          ))}
        </ul>
      </aside>
      <main className="flex-1 p-6 bg-gray-100 overflow-y-auto">
        <EmailList selectedFolder={selectedFolder} />
      </main>
    </div>
  );
}
