import React from "react";
import { connect } from "react-redux";
import { Dropdown } from "semantic-ui-react";
import { Link } from "react-router-dom";

import { indexTracks, queryCards, clearResults } from "../../actions";

import "../../styles/styles.css";

class ResultsPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      filter: {
        date: {},
        track: [],
      },
    };
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  componentWillMount() {
    this.props.indexTracks();
  }

  componentWillUnmount() {
    this.props.clearResults();
  }

  handleSubmit(e) {
    e.preventDefault();
    this.props.queryCards(this.buildFilter());
  }

  handleFilterEvent(field, e) {
    const filter = this.state.filter;
    const fieldElements = field.split(">");
    let pointer = filter;
    let current_el;
    for (const el of fieldElements) {
      if (!!current_el) {
        pointer = pointer[current_el];
      }
      current_el = el;
    }
    pointer[current_el] = e.target.value;
    this.setState({
      filter,
    });
  }

  handleDropdownChange(field, event, { value }) {
    const filter = this.state.filter;
    filter[field] = value;
    this.setState({
      filter,
    });
  }

  handleMultiSelect(field, e) {
    var options = e.target.options;
    var value = [];
    for (var i = 0, l = options.length; i < l; i++) {
      if (options[i].selected) {
        value.push(options[i].value);
      }
    }
    this.setState({ value: value });
  }

  buildFilter() {
    const stateElements = this.state.filter;
    let filter = [];
    if (Object.keys(stateElements.date).length > 0) {
      if (stateElements.date["min"] !== undefined) {
        filter.push({
          field: "date",
          operator: "gte",
          arguments: [stateElements.date["min"]],
        });
      }
      if (stateElements.date["max"] !== undefined) {
        filter.push({
          field: "date",
          operator: "lte",
          arguments: [stateElements.date["max"]],
        });
      }
    }
    if (stateElements.track.length > 0) {
      filter.push({
        field: "track_id",
        operator: "in",
        arguments: stateElements.track,
      });
    }
    return filter;
  }

  renderedFilters() {
    return (
      <div className="ui form">
        <div className="ui two column stackable grid">
          <div className="column">
            <div className="field">
              <label>
                Start Date:
                <input
                  type="date"
                  value={this.state.filter.date.min}
                  onChange={this.handleFilterEvent.bind(this, "date>min")}
                ></input>
              </label>
            </div>
          </div>
          <div className="column">
            <div className="field">
              <label>
                End Date:
                <input
                  type="date"
                  value={this.state.filter.date.max}
                  onChange={this.handleFilterEvent.bind(this, "date>max")}
                ></input>
              </label>
            </div>
          </div>
          <div className="four column row">
            <div className="column">
              <div className="field">
                <label>Tracks</label>
                <Dropdown
                  placeholder="Select Tracks"
                  fluid
                  search
                  selection
                  multiple
                  options={this.props.trackIndex.map((track) => {
                    return {
                      key: track.id,
                      value: track.id,
                      text: track.code,
                    };
                  })}
                  onChange={this.handleDropdownChange.bind(this, "track")}
                />
              </div>
            </div>
          </div>
          <div className="row">
            <div className="column">
              <button onClick={this.handleSubmit}>Update Filter</button>
            </div>
          </div>
        </div>
        <div className="ui divider"></div>
      </div>
    );
  }

  renderedCard(card) {
    const key = card.track_code.toUpperCase() + " - " + card.date;
    return (
      <div className="six wide column race-card" key={key}>
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
            {card.races.map((race) => {
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
    return (
      <div className="ui stackable row">
        {this.props.cards.map((card) => {
          return this.renderedCard(card);
        })}
      </div>
    );
  }

  render() {
    return (
      <div>
        {this.renderedFilters()}
        {this.renderedCards()}
      </div>
    );
  }
}

const mapStatetoProps = (state) => {
  return {
    trackIndex: state.backend.trackIndex,
    cards: state.backend.cards,
  };
};

export default connect(mapStatetoProps, {
  indexTracks,
  queryCards,
  clearResults,
})(ResultsPage);
