import { useEffect, useState } from "react";

export default function EmailDashboard() {
    const [folders, setFolders] = useState([]);
    const [emails, setEmails] = useState({});
    const [selectedFolder, setSelectedFolder] = useState("");
    const [selectedEmail, setSelectedEmail] = useState(null);

    useEffect(() => {
        const fetchEmails = async () => {
            try {
                const response = await fetch("http://localhost:8000/api/mails");
                const data = await response.json();

                // Data is already in folder structure { Inbox: [...], Spam: [...], etc. }
                setFolders(Object.keys(data));
                setEmails(data);

                if (Object.keys(data).length > 0) {
                    setSelectedFolder(Object.keys(data)[0]);
                }
            } catch (error) {
                console.error("Failed to fetch emails:", error);
            }
        };

        fetchEmails();
    }, []);

    const fetchEmailDetail = async (folder, msgid) => {
        try {
            const response = await fetch(
                `http://localhost:8000/api/mail/${encodeURIComponent(folder)}/${msgid}`
            );
            const data = await response.json();
            setSelectedEmail(data);
        } catch (error) {
            console.error("Failed to fetch email detail:", error);
        }
    };

    return (
        <div className="flex min-h-screen">
            {/* Sidebar */}
            <aside className="w-64 bg-white shadow-md p-4">
                <h2 className="text-xl font-bold mb-6">Folders</h2>
                <ul className="space-y-2">
                    {folders.map((folder) => (
                        <li
                            key={folder}
                            onClick={() => {
                                setSelectedFolder(folder);
                                setSelectedEmail(null);
                            }}
                            className={`cursor-pointer px-3 py-2 rounded ${
                                selectedFolder === folder
                                    ? "bg-indigo-100 text-indigo-700"
                                    : "hover:bg-gray-100"
                            }`}
                        >
                            {folder}
                        </li>
                    ))}
                </ul>
            </aside>

            {/* Main Content */}
            <main className="flex-1 bg-gray-50 p-6 overflow-y-auto">
                {selectedEmail ? (
                    <div>
                        <button
                            onClick={() => setSelectedEmail(null)}
                            className="mb-4 text-indigo-600"
                        >
                            Back
                        </button>
                        <pre className="bg-white p-4 rounded shadow overflow-auto">
                            {selectedEmail.content}
                        </pre>
                    </div>
                ) : (
                    <>
                        <h1 className="text-2xl font-bold mb-4">{selectedFolder}</h1>
                        <div className="space-y-4">
                            {Array.isArray(emails[selectedFolder]) &&
                            emails[selectedFolder].length > 0 ? (
                                emails[selectedFolder].map((email) => (
                                    <div
                                        key={email.id}
                                        onClick={() => fetchEmailDetail(selectedFolder, email.id)}
                                        className="bg-white p-4 rounded shadow hover:bg-gray-100 cursor-pointer"
                                    >
                                        <h3 className="text-lg font-semibold">{email.subject}</h3>
                                        <p className="text-sm text-gray-500">From: {email.from}</p>
                                        <p className="text-sm text-gray-500">Date: {email.date}</p>
                                    </div>
                                ))
                            ) : (
                                <p className="text-gray-500">No emails in this folder.</p>
                            )}
                        </div>
                    </>
                )}
            </main>
        </div>
    );
}
