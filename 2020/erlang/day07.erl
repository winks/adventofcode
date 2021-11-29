-module(day07).
-export([start/0]).

% ../input/day06/
xread() ->
    {ok, File} = file:open("input.txt",[read]),
    file:read(File, 1024 * 1024).

strlist(X, Div) ->
    case X of
        {ok, S} ->
            string:split(string:trim(S), Div, all);
        _Else ->
            []
    end.

x(S, R1) ->
    {_,M1} = re:run(S, R1, [{capture, all, list}]),
    {_,M2} = re:run(S, R1, [{capture, all, list}]),
    erlang:display(S),
    erlang:display(M1).

start() ->
    L = strlist(xread(), "\n"),
    {_, R1} = re:compile("^(\\w+ \\w+) bags contain (no other|[^\\.]+) bags?\.$"),
    {_, R2} = re:compile("(\\d+) (\\w+ \\w+)( bags?)?"),
    x(hd(L), R1).
    
