/**
 * Netlify Function: Submit Translation Corrections to GitHub
 *
 * This function receives translation corrections from the tmaster forms
 * and securely commits them to the GitHub repository.
 *
 * Environment Variables Required:
 * - GITHUB_TOKEN: Personal access token with repo write permissions
 * - GITHUB_OWNER: Repository owner (e.g., 'scott009')
 * - GITHUB_REPO: Repository name (e.g., 'rdgtrans')
 */

const handler = async (event, context) => {
  // CORS headers for GitHub Pages
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Content-Type': 'application/json'
  };

  // Handle preflight requests FIRST
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers,
      body: ''
    };
  }

  // Only allow POST requests
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({ error: 'Method not allowed. Use POST.' })
    };
  }

  try {
    // Parse the incoming corrections data
    const corrections = JSON.parse(event.body);

    // Validate the data structure
    if (!corrections.metadata || !corrections.corrections) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({
          error: 'Invalid data structure. Expected metadata and corrections.'
        })
      };
    }

    const { language, editor, timestamp } = corrections.metadata;

    if (!language || !editor || !timestamp) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({
          error: 'Missing required metadata fields: language, editor, or timestamp.'
        })
      };
    }

    // Get environment variables
    const GITHUB_TOKEN = process.env.GITHUB_TOKEN;
    const GITHUB_OWNER = process.env.GITHUB_OWNER || 'scott009';
    const GITHUB_REPO = process.env.GITHUB_REPO || 'rdgtrans';

    if (!GITHUB_TOKEN) {
      console.error('GITHUB_TOKEN environment variable not set');
      return {
        statusCode: 500,
        headers,
        body: JSON.stringify({
          error: 'Server configuration error. Please contact administrator.'
        })
      };
    }

    // Create filename based on language and timestamp
    const date = timestamp.split('T')[0];
    const timeStr = timestamp.split('T')[1].split('.')[0].replace(/:/g, '-');
    const filename = `corrections/${language}_${date}_${timeStr}.json`;

    // Convert JSON to base64 for GitHub API
    const content = JSON.stringify(corrections, null, 2);
    const contentBase64 = Buffer.from(content).toString('base64');

    // Commit message
    const commitMessage = `Add ${language} corrections from ${editor} (${corrections.corrections.length} items)`;

    // GitHub API endpoint
    const apiUrl = `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents/${filename}`;

    // Check if file already exists (to get SHA for update)
    let sha = null;
    try {
      const checkResponse = await fetch(apiUrl, {
        method: 'GET',
        headers: {
          'Authorization': `token ${GITHUB_TOKEN}`,
          'Accept': 'application/vnd.github.v3+json',
          'User-Agent': 'RDG-Translation-Tool'
        }
      });

      if (checkResponse.ok) {
        const existing = await checkResponse.json();
        sha = existing.sha;
      }
    } catch (e) {
      // File doesn't exist, which is fine for new submissions
    }

    // Create or update file in GitHub
    const requestBody = {
      message: commitMessage,
      content: contentBase64,
      branch: 'master'
    };

    // If file exists, include SHA for update
    if (sha) {
      requestBody.sha = sha;
      requestBody.message = `Update ${language} corrections from ${editor} (${corrections.corrections.length} items)`;
    }

    const response = await fetch(apiUrl, {
      method: 'PUT',
      headers: {
        'Authorization': `token ${GITHUB_TOKEN}`,
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json',
        'User-Agent': 'RDG-Translation-Tool'
      },
      body: JSON.stringify(requestBody)
    });

    if (!response.ok) {
      const errorData = await response.text();
      console.error('GitHub API error:', errorData);
      return {
        statusCode: response.status,
        headers,
        body: JSON.stringify({
          error: 'Failed to commit to GitHub',
          details: errorData
        })
      };
    }

    const result = await response.json();

    // Return success response
    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        message: `Successfully saved ${corrections.corrections.length} corrections`,
        file: filename,
        commit_url: result.commit.html_url,
        download_url: result.content.download_url
      })
    };

  } catch (error) {
    console.error('Error processing corrections:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        error: 'Internal server error',
        message: error.message
      })
    };
  }
};

module.exports = { handler };
