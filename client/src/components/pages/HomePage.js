import React from "react";
import { connect } from "react-redux";
import { Link } from "react-router-dom";

import {
  fetchCards,
  fetchEntrants,
  fetchHotJockeys,
  fetchHotTrainers,
  clearHotJockeys,
  clearHotTrainers,
} from "../../actions";

import { TimeFrameSelector } from "../utils";

import "../../styles/styles.css";

class HomePage extends React.Component {
  constructor(props) {
    super(props);
    this.state = { isMobile: window.innerWidth < 781 };
    this.onTimeFrameSelect = this.onTimeFrameSelect.bind(this);
  }

  componentDidMount() {
    window.addEventListener("resize", this.throttledHandleWindowResize);
    this.props.fetchCards();
    this.props.fetchEntrants();
    this.props.fetchHotJockeys(90);
    this.props.fetchHotTrainers(90);
  }

  componentWillUnmount() {
    window.removeEventListener("resize", this.throttledHandleWindowResize);
  }

  onTimeFrameSelect(e, { name }) {
    this.props.clearHotJockeys();
    this.props.clearHotTrainers();
    if (name === "all_time") {
      this.props.fetchHotJockeys();
      this.props.fetchHotTrainers();
    } else {
      this.props.fetchHotJockeys(parseInt(name));
      this.props.fetchHotTrainers(parseInt(name));
    }
  }

  throttledHandleWindowResize = () => {
    return this.setState({ isMobile: window.innerWidth < 781 });
  };

  renderedPlaceholder() {
    return (
      <div className="ui placeholder">
        <div className="paragraph">
          <div className="line"></div>
          <div className="line"></div>
          <div className="line"></div>
          <div className="line"></div>
          <div className="line"></div>
          <div className="line"></div>
          <div className="line"></div>
          <div className="line"></div>
          <div className="line"></div>
          <div className="line"></div>
          <div className="line"></div>
          <div className="line"></div>
          <div className="line"></div>
          <div className="line"></div>
          <div className="line"></div>
          <div className="line"></div>
          <div className="line"></div>
        </div>
      </div>
    );
  }

  renderedCard(card) {
    const key = card.track_code.toUpperCase() + " - " + card.date;
    return (
      <div className="column race-card" key={key}>
        <div className="ui header center aligned">{key}</div>
        <table className="ui basic compact unstackable table">
          <thead>
            <tr>
              <th>Race</th>
              <th>Dist.</th>
              <th>Surf.</th>
              <th>Class</th>
              <th>Purse</th>
            </tr>
          </thead>
          <tbody>
            {card.races &&
              card.races.map((race) => {
                return (
                  <tr key={race.id} className="row-highlight">
                    <td data-label="Race">
                      <Link className="rowLink" to={`/races/${race.id}`}>
                        {race.race_number}
                      </Link>
                    </td>

                    <td data-label="Distance">
                      <Link className="rowLink" to={`/races/${race.id}`}>
                        {race.distance}
                      </Link>
                    </td>

                    <td data-label="Surface">
                      <Link className="rowLink" to={`/races/${race.id}`}>
                        {race.surface}
                      </Link>
                    </td>

                    <td data-label="Class">
                      <Link className="rowLink" to={`/races/${race.id}`}>
                        {race.classification}
                      </Link>
                    </td>

                    <td data-label="Purse">
                      <Link className="rowLink" to={`/races/${race.id}`}>
                        {race.purse}
                      </Link>
                    </td>
                  </tr>
                );
              })}
          </tbody>
        </table>
      </div>
    );
  }

  renderedCards() {
    if (this.props.cards.length > 0) {
      if (this.state.isMobile) {
        return (
          <div className="ui one column row">
            {this.props.cards.map((card) => {
              return this.renderedCard(card);
            })}
          </div>
        );
      } else {
        return (
          <div className="ui two column row scroll">
            {this.props.cards.map((card) => {
              return this.renderedCard(card);
            })}
          </div>
        );
      }
    } else {
      if (this.state.isMobile) {
        return this.renderedPlaceholder();
      } else {
        return (
          <div className="ui two column row scroll">
            <div className="column">{this.renderedPlaceholder()}</div>
            <div className="column">{this.renderedPlaceholder()}</div>
            <div className="column">{this.renderedPlaceholder()}</div>
          </div>
        );
      }
    }
  }

  renderedEntrantHeader() {
    if (this.props.entrants.length > 0) {
      return (
        <div className="ui row">
          <div className="left floated eight wide column">
            <h2 className="ui header">Upcoming Entries</h2>
          </div>
        </div>
      );
    } else {
      return null;
    }
  }

  renderedEntrants() {
    if (this.props.entrants.length > 0) {
      if (this.state.isMobile) {
        return (
          <div className="ui one column row">
            {this.props.entrants.map((card) => {
              return this.renderedCard(card);
            })}
          </div>
        );
      } else {
        return (
          <div className="ui two column row scroll">
            {this.props.entrants.map((card) => {
              return this.renderedCard(card);
            })}
          </div>
        );
      }
    } else {
      return null;
    }
  }

  renderedConnection(conn, type) {
    let linkTo;
    if (type === "j") {
      linkTo = `/jockeys/${conn.id}`;
    } else if (type === "t") {
      linkTo = `/trainers/${conn.id}`;
    }
    return (
      <tr key={`${type}-${conn.id}`}>
        <td className="cell-highlight" data-label="Name">
          <Link className="rowLink" to={linkTo}>
            {conn.full_name}
          </Link>
        </td>
        <td data-label="Starts">{conn.starts}</td>
        <td data-label="wins">{conn.wins}</td>
      </tr>
    );
  }

  renderedConnections() {
    const jockeys = this.props.hot_jockeys;
    const trainers = this.props.hot_trainers;
    if (trainers.length > 0 && jockeys.length > 0) {
      return (
        <div className="ui two column row">
          <div className="column">
            <h3>Jockeys</h3>
            <table className="ui basic compact unstackable table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Starts</th>
                  <th>Wins</th>
                </tr>
              </thead>
              <tbody>
                {jockeys.map((jockey) => {
                  return this.renderedConnection(jockey, "j");
                })}
              </tbody>
            </table>
          </div>
          <div className="column">
            <h3>Trainers</h3>
            <table className="ui basic compact unstackable table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Starts</th>
                  <th>Wins</th>
                </tr>
              </thead>
              <tbody>
                {trainers.map((trainer) => {
                  return this.renderedConnection(trainer, "t");
                })}
              </tbody>
            </table>
          </div>
        </div>
      );
    } else {
      return (
        <div className="ui two column row">
          <div className="column">{this.renderedPlaceholder()}</div>
          <div className="column">{this.renderedPlaceholder()}</div>
        </div>
      );
    }
  }

  render() {
    return (
      <div>
        <div className="ui relaxed grid">
          {this.renderedEntrantHeader()}
          {this.renderedEntrants()}
          <div className="ui row">
            <div className="left floated eight wide column">
              <h2 className="ui header">Recent Cards</h2>
            </div>
          </div>
          {this.renderedCards()}
          <div className="ui row">
            <div className="left floated eight wide column">
              <h2 className="ui header">Hot Connections</h2>
            </div>
          </div>
          <div className="row">
            <TimeFrameSelector onClick={this.onTimeFrameSelect} />
          </div>
          {this.renderedConnections()}
        </div>
      </div>
    );
  }
}

const mapStatetoProps = (state) => {
  return {
    cards: state.backend.cards,
    entrants: state.backend.entrants,
    hot_jockeys: state.backend.hot_jockeys,
    hot_trainers: state.backend.hot_trainers,
  };
};

export default connect(mapStatetoProps, {
  fetchCards,
  fetchEntrants,
  fetchHotJockeys,
  fetchHotTrainers,
  clearHotJockeys,
  clearHotTrainers,
})(HomePage);
