import React, { Component } from 'react';
import { createMemoryHistory } from 'react-router';
import fetchData from '../../lib/fetchData';

const BASE_GENE_URL = '/api/gene';

class Gene extends Component {
  render() {
    
    let tempHistory = createMemoryHistory('/');
    let qp = '1233';
    let geneUrl = tempHistory.createPath({ pathname: BASE_GENE_URL, query: qp });
    fetchData(geneUrl);
    
    return (
      <div>
        <h1>Gene</h1>
      </div>
    );
  }
}

export default Gene;
