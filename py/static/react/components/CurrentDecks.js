import React from 'react'
import PropTypes from 'prop-types'

export default class CurrentDecks extends React.Component {
	constructor(props) {
		super(props)
		this.state = {}
	}

	componentDidMount() {}

	render() {
		//console.log(this.props.deck_id,this.props.has_deck)
		return (
			<div className="row">
				<div className="col-xs-3">
				{this.props.has_deck == true ? (
					<button type="button" onClick={this.props.onUpClick}>
						<span className="glyphicon glyphicon-plus"  />
					</button>
				):
					<button type=  "button" disabled ={true} className = "disabled-button">
						<span className="glyphicon glyphicon-plus" />
					</button>
				}
				</div>
			</div>

		)
	}
}

CurrentDecks.propTypes = {
	deck_id: PropTypes.number,
	// min: PropTypes.number,
	// max: propTypes.number,
	// onChange: propTypes.function,
	onUpClick: PropTypes.function,
	has_deck: PropTypes.bool
}
