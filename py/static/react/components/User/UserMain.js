import React from 'react'
import SearchTab from './SearchTab'
import CollectionTab from './CollectionTab'
import DeckTab from './DeckTab'

const COLLECTION_INDEX = 0
const SEARCH_INDEX = 1
const DECK_INDEX = 2

export default class UserMain extends React.Component {
	constructor(props) {
		super(props)
		this.state = {
			search_query: '',
			tab_index: SEARCH_INDEX
		}
	}

	componentDidMount() {}

	render() {
		var tab_index = this.state.tab_index
		return (
			<div className="container">
				<div className="row">
					Welcome <b>{this.props.user.username}</b>
				</div>
				<div className="row">
					<ul className="nav nav-pills">
						<li
							role="presentation"
							onClick={() => this.setState({ tab_index: COLLECTION_INDEX })}
							className={tab_index == COLLECTION_INDEX ? 'active' : ''}
						>
							<a href="#">COLLECTION</a>
						</li>
						<li
							role="presentation"
							onClick={() => this.setState({ tab_index: SEARCH_INDEX })}
							className={(tab_index == SEARCH_INDEX) ? 'active' : ''}
						>
							<a href="#">SEARCH</a>
						</li>
						<li
							role="presentation"
							onClick={() => this.setState({ tab_index: DECK_INDEX })}
							className={tab_index == DECK_INDEX ? 'active' : ''}
						>
							<a href="#">DECKS</a>
						</li>
						<li role="presentation">
							<a href="#" onClick={() => this.props.updateUser(null)}>
								LOGOUT
							</a>
						</li>
					</ul>
				</div>
				<div className="row">
					<CollectionTab {...this.props} selected={tab_index == COLLECTION_INDEX} />
					<SearchTab {...this.props} selected={tab_index == SEARCH_INDEX} />
					<DeckTab {...this.props} selected={tab_index == DECK_INDEX} />
				</div>
			</div>
		)
	}
}
