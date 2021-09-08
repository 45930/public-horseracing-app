import React from "react";
import { connect } from "react-redux";
import { Link } from "react-router-dom";

import { fetchSimulcastRaces } from "../../actions";

import "../../styles/styles.css";

class SimulcastPage extends React.Component {
  constructor(props) {
    super(props);
  }

  componentWillMount() {
    this.props.fetchSimulcastRaces();
  }

  renderedRace(race) {
    return (
      <tr key={race.id} className="row-highlight">
        <td data-label="Post Time">
          <Link className="rowLink" to={`/races/${race.id}`}>
            {race.post_time}
          </Link>
        </td>

        <td data-label="Track">
          <Link className="rowLink" to={`/races/${race.id}`}>
            {race.track_code}
          </Link>
        </td>

        <td data-label="Race">
          <Link className="rowLink" to={`/races/${race.id}`}>
            {race.race_number}
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
  }

  renderedRaces() {
    const races = this.props.races;
    return (
      <table className="ui basic compact unstackable table">
        <thead>
          <tr>
            <th>Post Time</th>
            <th>Track</th>
            <th>Race Number</th>
            <th>Surface</th>
            <th>Class</th>
            <th>Purse</th>
          </tr>
        </thead>
        <tbody>
          {races.map((race) => {
            return this.renderedRace(race);
          })}
        </tbody>
      </table>
    );
  }

  render() {
    return (
      <div className="ui container">
        {this.renderedRaces()}
      </div>
    );
  }
}

const mapStatetoProps = (state) => {
  return {
    races: state.backend.simulcastRaces,
  };
};

export default connect(mapStatetoProps, {
  fetchSimulcastRaces,
})(SimulcastPage);
