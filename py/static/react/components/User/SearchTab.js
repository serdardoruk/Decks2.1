import React from 'react'
import QuantityCounter from '../QuantityCounter'
import { query_cards } from '../../api/CardService'
import { update_collection_card_quantity } from '../../api/UserService'

export default class SearchTab extends React.Component {
	constructor(props) {
		super(props)
		this.state = {
			search_query: '',
			queried_cards: []
		}
		this.onSearchQueryChange = this.onSearchQueryChange.bind(this)
		this.updateCardQuantity = this.updateCardQuantity.bind(this)
	}

	componentDidMount() {
		var form_data = { jwt: this.props.user.jwt, search_query: this.state.search_query }
		query_cards(form_data, this.handleSearchQueryResponse.bind(this))
	}

	onSearchQueryChange(event) {
		var new_query = event.target.value
		this.setState({ search_query: new_query })
		var form_data = { jwt: this.props.user.jwt, search_query: new_query }
		query_cards(form_data, this.handleSearchQueryResponse.bind(this))
	}

	handleSearchQueryResponse(response) {
		this.setState({ queried_cards: response.queried_cards })
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
		var form_data = { jwt: this.props.user.jwt, search_query: this.state.search_query }
		query_cards(form_data, this.handleSearchQueryResponse.bind(this))
	}

	render() {
		var tab_index = this.state.tab_index
		return (
			<div className={this.props.selected ? '' : 'hidden'}>
				<p className="tooltips"> This is the SearchTab. In this tab you can <b><i> add </i></b> or <b><i> remove </i></b> cards in your collection. <br/> These changes will <b> persist </b> throughout multiple sessions! </p>
				<div className="row">
					<form
						className="navbar-form navbar-left"
						role="search"
						onSubmit={e => e.preventDefault()}
					>
						<div className="form-group">
							<input
								onChange={this.onSearchQueryChange.bind(this)}
								type="text"
								className="form-control"
								placeholder="Search"
							/>
						</div>
					</form>
				</div>
				{this.state && this.state.queried_cards && this.state.queried_cards.length == 0 ? (
					<div>Enter to search cards</div>
				) : (
					<table className="table table-bordered">
						<thead>
							<tr>
								<th>Card Name</th>
								<th>Amount in Collection</th>
							</tr>
						</thead>
						<tbody>
							{this.state && this.state.queried_cards && this.state.queried_cards.map((card, index) => (
								<tr>
									<td>{card.card.name}</td>
									<td>
										<QuantityCounter
											key = {card.card_id}
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
