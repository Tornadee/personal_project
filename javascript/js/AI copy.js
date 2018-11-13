var AI = {
  init: async function() {
    this.model = await tf.loadModel("http://localhost:8888/fetch_json");
    console.log("loaded");
  },
  returnState: async function() {
    // player absolute position
    var p_z = player.position.z * (-1);
    var p_x = player.position.x * (-1) * 1.3;
    var p_r = rotation;
    // relative nearest block observation
    let p_at_ind = Math.round(player.position.z/(-2.0));
    block_ind_1 = p_at_ind +0;
    block_ind_2 = p_at_ind +1;
    block_ind_3 = p_at_ind +2;
    b_1_x = platforms_data[block_ind_1];
    b_2_x = platforms_data[block_ind_2];
    b_3_x = platforms_data[block_ind_3];
    d_1_x = p_x - b_1_x;
    d_2_x = p_x - b_2_x;
    d_3_x = p_x - b_3_x;
    // data normalization
    p_z   /= 10;
    p_x   /= 2;
    d_1_x /= 2;
    d_2_x /= 2;
    d_3_x /= 2;
    p_x   += 0.5;
    d_1_x += 0.5;
    d_2_x += 0.5;
    d_3_x += 0.5;
    var observation = [p_x, p_z, p_r, d_1_x, d_2_x, d_3_x];
    return observation;
  },
  choose_action: async function() {
    // input
    var observation = await this.returnState();
    observation[1] = 10;
    //observation[0] = 3;
    if (!(isNaN(observation[3]))) {
        let input_tensor = await tf.tensor([observation]); //.expandDims(1);
        // prediction
        var prediction = await this.model.predict(input_tensor);
        var action_index = await prediction.argMax(1).dataSync()[0]; // axis = 1
        var action_value = action_index - 1; // 0,1,2 --> -1,0,1
        // logging
        $("#label_state").html(JSON.stringify(observation).split(",").join("<br>"));
        $("#label_pred1").text("Turn left:"+prediction.dataSync()[0]);
        $("#label_pred2").text("Go straight:"+prediction.dataSync()[1]);
        $("#label_pred3").text("Turn right:"+prediction.dataSync()[2]);
        $("#label_index").text("Index of best action: "+action_index);
        //console.log(action_index,action_value);
        return action_value;
    } else {
        return 0;
    }
  }
}
