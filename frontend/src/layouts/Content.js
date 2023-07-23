import React from "react";
import { Switch, Route, Redirect } from "react-router-dom";

// components

import AdminNavbar from "components/Navbars/AdminNavbar.js";
// import Sidebar from "components/Sidebar/Sidebar.js";
import AuthorSidebar from "components/Sidebar/AuthorSidebar.js";
import HeaderStats from "components/Headers/HeaderStats.js";
import FooterAdmin from "components/Footers/FooterAdmin.js";

// views

import ContentDashboard from "views/content/ContentDashboard.js";
import Maps from "views/content/Maps.js";
import Settings from "views/content/Settings.js";
import Tables from "views/content/Tables.js";

export default function Content() {
  return (
    <>
      <AuthorSidebar />
      <div className="relative md:ml-64 bg-blueGray-100">
        <AdminNavbar />
        {/* Header */}
        <HeaderStats />
        <div className="px-4 md:px-10 mx-auto w-full -m-24">
          <Switch>
            <Route path="/content/info" exact component={ContentDashboard} />
            <Route path="/content/maps" exact component={Maps} />
            <Route path="/content/settings" exact component={Settings} />
            <Route path="/content/tables" exact component={Tables} />
            <Redirect from="/content" to="/content/dashboard" />
          </Switch>
          <FooterAdmin />
        </div>
      </div>
    </>
  );
}
