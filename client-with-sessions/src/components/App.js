import React, { useEffect, useState } from "react";
import NavBar from "./NavBar";
import Login from "../pages/Login";
import Notes from "./Notes";

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
   fetch(`${process.env.REACT_APP_API_URL}/check_session`, {
        credentials: "include",
    }).then((r) => {
      if (r.ok) {
        r.json().then((user) => setUser(user));
      }
    });
  }, []);

  if (!user) return <Login onLogin={setUser} />;

  return (
    <>
      <NavBar user={user} setUser={setUser} />
      <main>
        <Notes />
      </main>
    </>
  );
}

export default App;
