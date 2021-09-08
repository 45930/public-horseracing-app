import React from "react";
import { connect } from "react-redux";
import { Dropdown } from "semantic-ui-react";

import { listEntries, scratchEntry, indexTracks } from "../../actions";

import "../../styles/styles.css";

class EnterScratchesPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      track: [],
    };
    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleScratch = this.handleScratch.bind(this);
  }

  componentWillMount() {
    this.props.indexTracks();
  }

  handleInputChange(event, { value }) {
    event.preventDefault();
    const track = value;
    this.setState({ track });
  }

  handleSubmit(e) {
    e.preventDefault();
    this.props.listEntries(this.state.track);
  }

  handleScratch(entry, e) {
    e.preventDefault();
    this.props.scratchEntry(entry.id);
    this.props.listEntries(this.state.track);
  }

  renderedInput() {
    return (
      <div className="ui form">
        <div className="field">
          <label>
            Track:
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
              onChange={this.handleInputChange}
            />
          </label>
        </div>
        <button onClick={this.handleSubmit}>Update Filter</button>
      </div>
    );
  }

  renderedEntry(entry) {
    return (
      <tr key={entry.id}>
        <td data-label="Track">{entry.code}</td>
        <td data-label="Race Number">{entry.race_number}</td>
        <td data-label="Program Number">{entry.program_number}</td>
        <td data-label="Horse Name">{entry.name}</td>
        <td data-label="Scratch">
          <button onClick={this.handleScratch.bind(this, entry)}>
            Scratch
          </button>
        </td>
      </tr>
    );
  }

  renderedEntries() {
    const entries = this.props.entries;
    return (
      <table className="ui basic compact unstackable table">
        <thead>
          <tr>
            <th>Track</th>
            <th>Race Number</th>
            <th>Program Number</th>
            <th>Horse Name</th>
            <th>Scratch?</th>
          </tr>
        </thead>
        <tbody>
          {entries.map((entry) => {
            return this.renderedEntry(entry);
          })}
        </tbody>
      </table>
    );
  }

  render() {
    return (
      <div className="ui container">
        {this.renderedInput()}
        {this.renderedEntries()}
      </div>
    );
  }
}

const mapStatetoProps = (state) => {
  return {
    trackIndex: state.backend.trackIndex,
    entries: state.backend.entries,
  };
};

export default connect(mapStatetoProps, {
  indexTracks,
  listEntries,
  scratchEntry,
})(EnterScratchesPage);
