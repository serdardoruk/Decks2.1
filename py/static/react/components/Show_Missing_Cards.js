import React from 'react'
import PropTypes from 'prop-types'

export default class Show_Missing_Cards extends React.Component {
	constructor(props) {
		super(props)
		this.state = {
			show_cards: false
		}
	}

	componentDidMount() {}

	render() {
		return (
				<div>
				<div className={this.state.show_cards ? 'hidden' : ''}>
					<button type="button" onClick={() => this.setState({show_cards: true})}>
						<span className="glyphicon glyphicon-plus" />
					</button>
				</div>
				<div className={this.state.show_cards ? '' : 'hidden'}>
					<button type="button" onClick={() => this.setState({show_cards: false})}>
						<span className="glyphicon glyphicon-minus" />
					{this.state.show_cards == true && this.props.missing_cards ? (this.props.missing_cards.map((card,index) =>(
						<span> <br/> {card.quantity} {card.card.name} </span> 
						))) : <span/>
					}
					</button>
				</div>
				</div>
		)
	}
}

Show_Missing_Cards.propTypes = {
	deck_id: PropTypes.number,
	missing_cards: PropTypes.object,
}
