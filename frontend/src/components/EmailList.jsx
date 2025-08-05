import React, { useEffect, useState } from 'react';
import { fetchEmails } from '../api/emailService';

export default function EmailList() {
  const [emails, setEmails] = useState([]);

  useEffect(() => {
    const loadEmails = async () => {
      try {
        const data = await fetchEmails();
        setEmails(data);
      } catch (error) {
        console.error('Failed to fetch emails:', error);
      }
    };

    loadEmails();
  }, []);

  return (
    <div>
      <h2>Your Emails</h2>
      <ul>
        {emails.map((email, index) => (
          <li key={index}>
            {email.subject} - {email.from}
          </li>
        ))}
      </ul>
    </div>
  );
}
