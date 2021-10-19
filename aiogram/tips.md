* Handler cannot receive message and call at the same time as arguments
* ReplyKeyboard needs to be removed (reason why Inline is better)
* Handler is called if state was set OR text/callback/command was sent
* call has message method, so it possible to answer() inside callback handler

### FSM memory:

put data:

    # Method 1 (recommended if data["some_digit"] += 1 is needed
    async with state.proxy() as data:
        data['answer1'] = answer

    # Method 2
    await state.update_data(answer1=answer)

    # Method 3
    await state.update_data(
        {"answer1": answer}
    )

get data:

    data = await state.get_data()
    answer1 = data.get("answer1")

