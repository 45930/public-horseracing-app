import React from "react";
import { BrowserRouter, Route } from "react-router-dom";

import {
  HomePage,
  ExplorePage,
  ResultsPage,
  RaceDetailPage,
  HorseDetailPage,
  TrainerDetailPage,
  JockeyDetailPage,
  OwnerDetailPage,
  SearchPage,
  EnterScratchesPage,
  SimulcastPage,
} from "./pages";
import { Header } from "./utils";

const App = () => {
  return (
    <div className="ui container">
      <BrowserRouter>
        <Header />
        <div>
          <Route path="/" exact component={HomePage} />
          <Route path="/races/:id" exact component={RaceDetailPage} />
          <Route path="/horses/:id" exact component={HorseDetailPage} />
          <Route path="/trainers/:id" exact component={TrainerDetailPage} />
          <Route path="/jockeys/:id" exact component={JockeyDetailPage} />
          <Route path="/owners/:id" exact component={OwnerDetailPage} />
          <Route path="/explore" exact component={ExplorePage} />
          <Route path="/results" exact component={ResultsPage} />
          <Route path="/search" exact component={SearchPage} />
          <Route path="/scratches" exact component={EnterScratchesPage} />
          <Route path="/simulcast" exact component={SimulcastPage} />
        </div>
      </BrowserRouter>
    </div>
  );
};

export default App;
