import React from 'react'
import QuantityCounter from '../QuantityCounter'
import { update_collection_card_quantity } from '../../api/UserService'

// given a collection and a set of filter TBD, we filter the collection
// and return the filtered result
function filter_collection(collection, text_filter) {
	if (!text_filter) return collection
	var new_collection = []

	collection.map((card, index) => {
		if (card.card.name.toLowerCase().indexOf(text_filter.toLowerCase()) !== -1) {
			new_collection.push(card)
		}
	})
	return new_collection
}

export default class SearchTab extends React.Component {
	constructor(props) {
		super(props)
		this.state = {
			text_filter: '',
			displayed_collection: this.props.user.collection
		}
		this.onTextFilterChange = this.onTextFilterChange.bind(this)
	}

	componentDidMount() {}

	componentWillReceiveProps(nextProps) {
		var displayed_collection = filter_collection(
			nextProps.user.collection,
			this.state.text_filter
		)
		this.setState({ displayed_collection: displayed_collection })
	}

	onTextFilterChange(event) {
		this.setState({ text_filter: event.target.value })
		var displayed_collection = filter_collection(this.props.user.collection, event.target.value)
		this.setState({ displayed_collection: displayed_collection })
	}

	updateCardQuantity(card, new_quantity) {
		var form_data = {
			jwt: this.props.user.jwt,
			new_quantity: new_quantity,
			card_id: card.card.card_id
		}
		update_collection_card_quantity(form_data, this.handleUpdateCardQuantityResponse.bind(this))
	}

	handleUpdateCardQuantityResponse(response) {
		this.props.updateUser(response.user)
		var displayed_collection = filter_collection(
			this.props.user.collection,
			this.state.text_filter
		)
		this.setState({ displayed_collection: displayed_collection })
	}

	render() {
		var tab_index = this.state.tab_index
		return (
			<div className={this.props.selected ? '' : 'hidden'}>
				<p className="tooltips"> This is the collection tab and it contains your collection of cards. Your collection can be used to make <b><i>decks</i></b> over in the Decks Tab!</p>
				<div className="row">
					<form
						className="navbar-form navbar-left"
						role="search"
						onSubmit={e => e.preventDefault()}
					>
						<div className="form-group">
							<input
								onChange={this.onTextFilterChange.bind(this)}
								type="text"
								className="form-control"
								placeholder="Search"
							/>
						</div>
					</form>
				</div>
				{this.state.displayed_collection.length == 0 ? (
					<div>No cards to display!</div>
				) : (
					<table className="table table-bordered">
						<thead>
							<tr>
								<th>Card Name</th>
								<th>Amount in Collection</th>
							</tr>
						</thead>
						<tbody>
							{this.state.displayed_collection.map((card, index) => (
								<tr>
									<td>{card.card.name}</td>
									<td>
										<QuantityCounter
											value={card.quantity}
											onDownClick={() =>
												this.updateCardQuantity(
													card,
													Math.max(card.quantity - 1, 0)
												)
											}
											onUpClick={() =>
												this.updateCardQuantity(
													card,
													Math.min(card.quantity + 1, 100)
												)
											}
										/>
									</td>
								</tr>
							))}
						</tbody>
					</table>
				)}
			</div>
		)
	}
}
