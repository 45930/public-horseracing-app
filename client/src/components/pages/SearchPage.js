import React from "react";
import { connect } from "react-redux";
import { Link } from "react-router-dom";

import { searchHorses } from "../../actions";

import "../../styles/styles.css";

class SearchPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      term: "",
    };
    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleInputChange(e) {
    e.preventDefault();
    const term = e.target.value;
    this.setState({ term });
  }

  handleSubmit(e) {
    e.preventDefault();
    this.props.searchHorses(this.state.term);
  }

  renderedSearchInput() {
    return (
      <div className="ui form">
        <div className="field">
          <label>
            Horse Name:
            <input
              type="text"
              value={this.state.term}
              onChange={this.handleInputChange}
            ></input>
          </label>
        </div>
        <button onClick={this.handleSubmit}>Update Filter</button>
      </div>
    );
  }

  renderedSearchResult(result) {
    return (
      <tr key={result.id}>
        <td className="cell-highlight" data-label="Name">
          <Link className="rowLink" to={`/horses/${result.id}`}>
            {result.name}
          </Link>
        </td>
        <td data-label="Year Born">{result.year_born}</td>
        <td data-label="Month Born">{result.month_born}</td>
      </tr>
    );
  }

  renderedSearchResults() {
    const results = this.props.horse_search_results;
    return (
      <table className="ui basic compact unstackable table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Year Born</th>
            <th>Month Born</th>
          </tr>
        </thead>
        <tbody>
          {results.map((result) => {
            return this.renderedSearchResult(result);
          })}
        </tbody>
      </table>
    );
  }

  render() {
    return (
      <div className="ui container">
        {this.renderedSearchInput()}
        {this.renderedSearchResults()}
      </div>
    );
  }
}

const mapStatetoProps = (state) => {
  return {
    horse_search_results: state.backend.horse_search_results,
  };
};

export default connect(mapStatetoProps, {
  searchHorses,
})(SearchPage);
