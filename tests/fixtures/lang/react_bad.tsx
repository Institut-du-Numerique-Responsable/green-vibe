// Fixture: non-conforming React
import React, { useEffect, useState } from 'react';
export function Orders({ rows }) {
  const [data, setData] = useState([]);
  useEffect(() => { fetch('/api').then(r => r.json()).then(setData); });
  return <ul style={{ margin: 0 }}>{rows.map((r, index) => <li key={index}>{r.name}</li>)}</ul>;
}
