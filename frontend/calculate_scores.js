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

	// Iterate over all filenames and sum over arrays
	for (const filename of DB_FILENAMES) {
		// Normalize all scores to 0-1 for each feature
		wav_scores = normalize(wav_scores);
		edge_scores = normalize(edge_scores);
		color_scores = normalize(color_scores);

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
		ranked_files[min_filename] = final_scores[min_filename];

		// Convert score dists to actual scores
		ranked_files[min_filename] = ranked_files[min_filename];

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

wav_scores = {
    "StarCraft": [
        3470.97509765625,
        2714.0068359375,
        2210.4599609375,
        2198.9482421875,
        2193.0361328125,
        2196.278564453125,
        2210.817626953125,
        2193.9716796875,
        2126.19091796875,
        2093.2763671875,
        2003.0948486328125,
        2045.82275390625,
        2254.10546875,
        2378.726318359375,
        2360.945556640625,
        2382.51220703125,
        2363.512451171875,
        2425.9208984375,
        2354.880615234375,
        2318.40771484375,
        2253.59033203125,
        2144.45068359375,
        2170.8046875,
        2302.5146484375,
        2384.35302734375,
        2371.92138671875,
        2391.44677734375,
        2406.11669921875,
        2403.34619140625,
        2394.811767578125,
        2394.811767578125
    ],
    "flowers": [
        4932.74609375,
        4919.47509765625,
        5030.31640625,
        5146.52392578125,
        5264.47314453125,
        5348.06005859375,
        5479.0341796875,
        5447.74267578125,
        5446.10205078125,
        5526.37744140625,
        5612.0263671875,
        5634.298828125,
        5685.71337890625,
        5772.12255859375,
        5826.0419921875,
        5884.7900390625,
        5819.50390625,
        5784.81640625,
        5710.36328125,
        5643.5458984375,
        5583.0771484375,
        5619.35400390625,
        5639.630859375,
        5578.39306640625,
        5605.9228515625,
        5594.33056640625,
        5591.77587890625,
        5637.10595703125,
        5645.01220703125,
        5632.8193359375,
        5632.8193359375
    ],
    "interview": [
        3829.180419921875,
        3853.006591796875,
        4022.1220703125,
        4234.42041015625,
        4258.66015625,
        4285.650390625,
        4309.484375,
        4284.3154296875,
        4271.38330078125,
        4221.0224609375,
        4126.759765625,
        4143.18359375,
        4160.7080078125,
        4106.06884765625,
        4242.80126953125,
        4209.91064453125,
        4303.83544921875,
        4371.8759765625,
        4371.5947265625,
        4382.791015625,
        4354.3603515625,
        4357.22607421875,
        4373.0849609375,
        4297.03173828125,
        4120.72216796875,
        4165.3349609375,
        4063.333251953125,
        4135.673828125,
        4029.73046875,
        3912.908935546875,
        3912.908935546875
    ],
    "movie": [
        4762.8935546875,
        4777.3369140625,
        4830.85107421875,
        4751.80908203125,
        4610.6494140625,
        4653.30908203125,
        4636.0166015625,
        4666.0048828125,
        4562.81884765625,
        4493.9912109375,
        4477.826171875,
        4220.91552734375,
        4015.6845703125,
        3940.65380859375,
        3952.412109375,
        4033.61474609375,
        4031.49169921875,
        4049.933837890625,
        4317.888671875,
        4510.07763671875,
        4699.56103515625,
        4789.96630859375,
        4899.63134765625,
        4928.48095703125,
        4958.41015625,
        4957.6787109375,
        4935.78857421875,
        4899.8974609375,
        4769.474609375,
        4693.49072265625,
        4693.49072265625
    ],
    "musicvideo": [
        3171.60791015625,
        2520.24365234375,
        2049.878662109375,
        2084.980224609375,
        2232.819091796875,
        2311.4375,
        2360.938720703125,
        2356.501708984375,
        2466.765625,
        2520.914794921875,
        2496.048095703125,
        2464.125,
        2438.465087890625,
        2436.735595703125,
        2347.219970703125,
        2284.04248046875,
        2245.07958984375,
        2276.714111328125,
        2202.852294921875,
        2171.53076171875,
        2184.658203125,
        2209.47216796875,
        2276.857177734375,
        2238.420166015625,
        2196.708740234375,
        2211.128173828125,
        2247.7373046875,
        2212.435302734375,
        2220.130859375,
        2229.28759765625,
        2229.28759765625
    ],
    "sports": [
        1747.7509765625,
        1468.915283203125,
        1309.509521484375,
        1155.5406494140625,
        1015.950927734375,
        870.4674072265625,
        804.2977294921875,
        770.9039916992188,
        416.23565673828125,
        752.5447998046875,
        792.6282958984375,
        799.4188842773438,
        848.544921875,
        844.599365234375,
        826.4160766601562,
        847.4391479492188,
        836.1793823242188,
        827.0752563476562,
        825.4154663085938,
        814.9544067382812,
        802.7321166992188,
        762.7066040039062,
        753.5253295898438,
        724.4957885742188,
        722.484130859375,
        743.7205200195312,
        753.0142211914062,
        772.0634155273438,
        791.5341796875,
        842.0189208984375,
        842.0189208984375
    ],
    "traffic": [
        2060.42138671875,
        1473.62158203125,
        1487.398681640625,
        1483.4188232421875,
        1483.0223388671875,
        1465.6387939453125,
        1446.2286376953125,
        1457.5467529296875,
        1433.542236328125,
        1392.1998291015625,
        1413.6370849609375,
        1406.4991455078125,
        1399.6829833984375,
        1411.1861572265625,
        1403.05126953125,
        1384.239013671875,
        1400.00048828125,
        1418.7225341796875,
        1421.6444091796875,
        1415.9136962890625,
        1413.4246826171875,
        1405.4677734375,
        1406.572265625,
        1416.6566162109375,
        1424.8975830078125,
        1447.2061767578125,
        1448.2205810546875,
        1455.638671875,
        1453.651123046875,
        1466.2049560546875,
        1466.2049560546875
    ]
}

color_scores = {
   "traffic":[
      46130284.0,
      45965920.0,
      45776176.0,
      45500520.0,
      45206344.0,
      45020624.0,
      44757950.0,
      44602252.0,
      44275636.0,
      43870576.0,
      43466736.0,
      43155080.0,
      42985430.0,
      42955796.0,
      42948496.0,
      43114984.0,
      43354864.0,
      43542490.0,
      43903584.0,
      44348364.0,
      44866052.0,
      45320290.0,
      45742692.0,
      46118824.0,
      46093560.0,
      46012690.0,
      46381504.0,
      46754470.0,
      46895400.0,
      47075730.0,
      47366910.0
   ],
   "movie":[
      72207960.0,
      69270270.0,
      64904816.0,
      60442456.0,
      56673264.0,
      56350304.0,
      56311092.0,
      56218252.0,
      56043230.0,
      55847036.0,
      54809196.0,
      54851230.0,
      56996670.0,
      58960696.0,
      61095624.0,
      63904210.0,
      67207170.0,
      70937336.0,
      75137570.0,
      79457350.0,
      83504110.0,
      85146390.0,
      85749660.0,
      84794680.0,
      82736370.0,
      81029280.0,
      79297736.0,
      76645900.0,
      73507110.0,
      70305736.0,
      67024850.0
   ],
   "StarCraft":[
      63284016.0,
      62185730.0,
      62033010.0,
      62068176.0,
      62153784.0,
      62876990.0,
      63353170.0,
      63278000.0,
      63267960.0,
      63255896.0,
      62832400.0,
      62644264.0,
      62138904.0,
      60939550.0,
      58902924.0,
      56914160.0,
      54852880.0,
      52400170.0,
      50191996.0,
      48546584.0,
      47511252.0,
      46698130.0,
      45925536.0,
      46645450.0,
      47811172.0,
      49910560.0,
      52052880.0,
      53802920.0,
      55156936.0,
      55990520.0,
      56442544.0
   ],
   "flowers":[
      39279590.0,
      38559864.0,
      37849436.0,
      37350244.0,
      36920590.0,
      36420184.0,
      36038332.0,
      35736396.0,
      35467290.0,
      35286612.0,
      35135950.0,
      35227350.0,
      35662870.0,
      36134012.0,
      36457370.0,
      36849850.0,
      37054050.0,
      36758570.0,
      36239000.0,
      35380770.0,
      34236810.0,
      33550046.0,
      33137538.0,
      32839558.0,
      32553888.0,
      32352342.0,
      32132032.0,
      31888788.0,
      31596186.0,
      31510460.0,
      31486462.0
   ],
   "sports":[
      16077478.0,
      16379412.0,
      16537800.0,
      16704044.0,
      16096792.0,
      14308374.0,
      12184542.0,
      8694096.0,
      1529424.0,
      8955524.0,
      13069892.0,
      16414510.0,
      18306418.0,
      20403552.0,
      23547784.0,
      26280830.0,
      28574498.0,
      29087800.0,
      28277348.0,
      26983892.0,
      26033780.0,
      24622402.0,
      23596594.0,
      24089528.0,
      25009338.0,
      26010452.0,
      26285736.0,
      26440996.0,
      26905726.0,
      28187430.0,
      29814386.0
   ],
   "interview":[
      31390164.0,
      31438888.0,
      31394100.0,
      31617222.0,
      32063118.0,
      32600062.0,
      33223396.0,
      33834480.0,
      34295976.0,
      34259460.0,
      34110176.0,
      33964050.0,
      33806496.0,
      33676972.0,
      33685524.0,
      33663480.0,
      33659424.0,
      33635220.0,
      33608670.0,
      33630092.0,
      33707890.0,
      33764360.0,
      33749864.0,
      33602724.0,
      33559104.0,
      33487634.0,
      33378024.0,
      33347326.0,
      33294248.0,
      32828200.0,
      32363006.0
   ],
   "musicvideo":[
      61155896.0,
      56256250.0,
      53754056.0,
      50982572.0,
      48276310.0,
      45846840.0,
      45150610.0,
      44565256.0,
      43009170.0,
      42951410.0,
      43894624.0,
      45957324.0,
      47668896.0,
      49813544.0,
      51418240.0,
      52321136.0,
      51594110.0,
      53863836.0,
      55566070.0,
      54407864.0,
      53490600.0,
      52304200.0,
      50995948.0,
      49567664.0,
      49905372.0,
      49245744.0,
      49265856.0,
      46841704.0,
      46705776.0,
      47776400.0,
      48679340.0
   ]
}

edge_scores = {
   "traffic":[
      485450.15122564335,
      486142.0345691164,
      487338.0247836198,
      488446.22646715166,
      489957.5998747239,
      490991.2265000262,
      492562.3855157842,
      493362.530929336,
      493680.85614595184,
      495138.89165061555,
      495364.5253245331,
      495642.4707891768,
      496018.65617635794,
      494970.764818489,
      494467.1591218167,
      493129.25633144093,
      490855.26194082916,
      489660.492356694,
      489215.42317776533,
      488968.46769500384,
      488900.6411327357,
      488423.92731621984,
      488368.874008162,
      488957.29690843145,
      490011.8111841795,
      492160.70195618016,
      494309.3276987599,
      495743.3482155863,
      495471.10263869073,
      494153.74867039104,
      493149.6945147589
   ],
   "movie":[
      452723.3977551856,
      456803.37298995507,
      457854.11549422593,
      459421.05271199753,
      460954.6630092812,
      458526.73100921826,
      456129.6417686533,
      454895.98591326346,
      455865.04836958053,
      457650.4827922724,
      458467.5912210153,
      457330.2545753998,
      456050.586421068,
      455918.1790080321,
      456077.0347759247,
      455694.1325329963,
      455247.4942270413,
      451675.54784933844,
      445904.3046719778,
      439865.83468712366,
      433798.2474030987,
      429807.24671066215,
      426869.84767022374,
      425437.3719479754,
      425668.942048865,
      425693.3828766898,
      426265.2032772556,
      427687.30449359847,
      428665.5427019998,
      430231.10007878323,
      431703.7033371384
   ],
   "StarCraft":[
      477424.4267420761,
      480495.1812193334,
      479879.10633825266,
      483880.4907722567,
      488652.92775138473,
      492504.4940911707,
      496914.856288278,
      497584.91797883104,
      496979.3648130675,
      497848.366900003,
      499001.9023260332,
      500304.6062400385,
      503146.0824154353,
      500281.79584110394,
      494750.07736229815,
      489479.9227751839,
      482319.8779078051,
      475099.62836756674,
      468604.7378921814,
      461614.0977591564,
      454032.85274856485,
      446542.06156867236,
      439256.3562715968,
      433941.1505319587,
      430829.4239603419,
      436995.159870221,
      443970.6717509615,
      451598.52056334284,
      459021.9578081205,
      462572.95203027164,
      465905.5865730738
   ],
   "flowers":[
      554267.0051518491,
      558337.276294535,
      561334.5877237568,
      562596.7514792456,
      561650.5682361587,
      557847.980300189,
      551891.6993622934,
      545509.7296794989,
      538294.5510591761,
      531119.0906708213,
      524187.03334306163,
      519365.0799774663,
      516080.75320147333,
      514522.64425387536,
      513213.4586602343,
      511971.3562055987,
      511997.0113926447,
      512593.25936847826,
      515326.7359889258,
      519464.9807253613,
      525269.4238674092,
      529140.9142185095,
      531804.1353966703,
      534684.5934754432,
      538106.556269295,
      542115.7865022933,
      547156.9173006953,
      552008.9787313247,
      556842.8174539023,
      561227.3096304206,
      564451.7592983479
   ],
   "sports":[
      535964.1417109917,
      537389.1320542312,
      538134.348838652,
      537642.449914439,
      534970.1271332821,
      525026.2988413057,
      514510.25893562124,
      502903.57569816505,
      71441.88057435218,
      488791.6999602182,
      483730.16075597354,
      475499.31435281795,
      469013.0089347203,
      465185.0735728738,
      468996.0942801123,
      479091.52708537853,
      485649.96028518316,
      489605.511687726,
      490635.7715760236,
      491803.5801516699,
      494763.41732690786,
      497979.0271186127,
      500796.17433143395,
      502380.3531439103,
      498889.88820179546,
      493524.55197284766,
      491063.994785812,
      490366.92277314136,
      491103.7843470563,
      493377.358165127,
      495913.57331696415
   ],
   "interview":[
      487172.41131862137,
      486279.58439564373,
      485128.4358548775,
      484218.210159428,
      483748.3748809912,
      483746.8290593748,
      483703.7456956479,
      483377.1686530095,
      482992.7528959415,
      483080.72516402474,
      483604.1889551826,
      484100.62618736614,
      484807.64706221374,
      485266.7419832107,
      484605.9476265226,
      483536.95471494214,
      482559.18642172794,
      481941.7697709963,
      481345.5813134675,
      480685.6192460931,
      479843.06121897814,
      479077.3435469475,
      478247.45231940335,
      477640.050063853,
      477644.20225728693,
      477952.24879165494,
      477784.062443485,
      477557.13477551565,
      477505.9352248933,
      479074.1538895623,
      480826.6909188798
   ],
   "musicvideo":[
      451661.7270978359,
      455348.966755169,
      451203.4592620052,
      446969.53990177,
      442585.1727351471,
      439612.234560186,
      440429.44188030844,
      439838.18976414495,
      437917.6407156944,
      435225.0925383324,
      432914.0790330109,
      432095.1486362697,
      444885.0467817501,
      454385.1003279047,
      458514.96038842615,
      462168.3482238912,
      464662.97036131466,
      466914.6094041179,
      471918.95893256925,
      472248.0897526214,
      471559.19384526904,
      469879.7616678122,
      459138.5999074789,
      453289.81035867106,
      453506.01159190823,
      452981.78754779976,
      451981.00806339196,
      453315.34396598575,
      452759.80668562,
      456812.3408195098,
      458312.6144620067
   ]
}

final_scores = calculate_cum_scores(wav_scores, edge_scores, color_scores);
ranked_files = get_top_ranked_files(final_scores);
ranked_scores = convert_dist_to_scores(ranked_files)
console.log(ranked_scores);