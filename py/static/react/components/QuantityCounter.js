import React from 'react'
import PropTypes from 'prop-types'

export default class QuantityCounter extends React.Component {
	constructor(props) {
		super(props)
		this.state = {}
	}

	componentDidMount() {}

	render() {
		return (
			<div className="row">
				<div className="col-xs-3">
					<button type="button" onClick={this.props.onDownClick}>
						<span className="glyphicon glyphicon-minus" />
					</button>
				</div>
				<div className="col-xs-6">{this.props.value}</div>
				<div className="col-xs-3">
					<button type="button" onClick={this.props.onUpClick}>
						<span className="glyphicon glyphicon-plus" />
					</button>
				</div>
			</div>
		)
	}
}

QuantityCounter.propTypes = {
	value: PropTypes.number,
	// min: PropTypes.number,
	// max: propTypes.number,
	// onChange: propTypes.function,
	onUpClick: PropTypes.function,
	onDownClick: PropTypes.function
}
