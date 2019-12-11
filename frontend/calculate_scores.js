const DB_FILENAMES = ['sports', 'movie', 'interview', 'StarCraft', 'musicvideo', 'flowers', 'traffic'];

function normalize(scores) {
	let overall_min = Number.MAX_VALUE;
	let overall_max = Number.MIN_VALUE;

	scores_keys = Object.keys(scores);

	// First pass, get overall min and max
	for (const filename of scores_keys) {
		overall_min = Math.min(...scores[filename], overall_min);
		overall_max = Math.max(...scores[filename], overall_max);
	}

	let num_timestamps = scores[scores_keys[0]].length; // All score arrays should have the same #
	for (const filename of scores_keys) {
		// For all timestamps, normalize
		for (i = 0; i < num_timestamps; i++) {
			scores[filename][i] = (scores[filename][i] - overall_min) / (overall_max - overall_min);
		}
	}

	return scores;
}

function calculate_cum_scores(wav_scores, edge_scores, color_scores) {
	let num_timestamps = wav_scores['sports'].length; // All score arrays should have the same #
	var final_scores = {};

  // Normalize all scores to 0-1 for each feature 

  wav_scores = normalize(wav_scores);
  edge_scores = normalize(edge_scores);
  color_scores = normalize(color_scores);

	// Iterate over all filenames and sum over arrays
	for (const filename of DB_FILENAMES) {
		// Init empty cumulate scores array
		var filename_cum_scores = [];
		for (var i = 0; i < num_timestamps; i++) {
			filename_cum_scores.push(0);
		}

		// For all timestamps, get cum scores
		for (i = 0; i < num_timestamps; i++) {
			filename_cum_scores[i] += wav_scores[filename][i];
			filename_cum_scores[i] += edge_scores[filename][i];
			filename_cum_scores[i] += color_scores[filename][i];
		}

		final_scores[filename] = filename_cum_scores;
	}

	return final_scores;
}

function indexOfMin(arr) {
    if (arr.length === 0) {
        return -1;
    }

    var min = arr[0];
    var minIndex = 0;

    for (var i = 1; i < arr.length; i++) {
        if (arr[i] < min) {
            minIndex = i;
            min = arr[i];
        }
    }

    return minIndex;
}

function get_top_ranked_files(final_scores) {
	// Get lowest score for each filename
	var min_scores = [];
	for (const filename of DB_FILENAMES) {
		min_scores.push(Math.min(...final_scores[filename]));
	}
	
	// Sort and get top 3 ranked
	var ranked_files = {};
	var num_ranked = 0;

	while (num_ranked < 3) {
		let min_score =  Math.min(...min_scores);
		let min_idx = indexOfMin(min_scores);

		min_filename = DB_FILENAMES[min_idx];

    // Convert score dists to actual scores
		ranked_files[min_filename] = final_scores[min_filename];

		// Increment num ranked
		num_ranked++;

		// Remove curr one and continue (hack - set min to very high)
		min_scores[min_idx] = Number.MAX_VALUE;
	}

	return ranked_files;
}

function convert_dist_to_scores(dists) {
	dists = normalize(dists);
	dists_keys = Object.keys(dists);

	let num_timestamps = dists[scores_keys[0]].length;
	for (const filename of dists_keys) {
		// For all timestamps, normalize
		for (i = 0; i < num_timestamps; i++) {
			dists[filename][i] = 1 - dists[filename][i];
		}
	}

	return dists;
}

function convert_ranked_scores_to_hist(final_scores) {
    // Find key with largest value in list (top scoring video)
    key_with_largest_value = '';
    largest_value = Number.NEGATIVE_INFINITY;
    for (const k in final_scores) {
        for (const v in final_scores[k]) {
            if (final_scores[k][v] > largest_value) {
                largest_value = final_scores[k][v]
                key_with_largest_value = k
            }
        }
    }

    // Make histogram with final_scores[key_with_largest_value]

}
