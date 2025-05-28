#!/usr/bin/env escript
%%% -*- erlang -*-
%%% @author Tony Rogvall <tony@rogvall.se>
%%% @copyright (C) 2025, Tony Rogvall
%%% @doc
%%%    List burner aliases
%%% @end
%%% Created : 26 May 2025 by Tony Rogvall <tony@rogvall.se>

-mode(compile).
%%-module(burner_action).
-export([main/1]).

-define(BURNER_CONFIG_LINUX, "/var/www/data/burner.config").
-define(BURNER_CONFIG_MACOS, "/Library/WebServer/data/burner.config").

-define(DOMAIN, "rogvall.se").
%%-define(TMP1, "/var/www/data/tmp1.txt").
%%-define(TMP2, "/var/www/data/tmp2.txt").

main([]) ->
    Query = os:getenv("QUERY_STRING"),
    case Query of
	false ->
	    list_config(burner_config(), 
			{error,"1,missing alias"}),
	    erlang:halt(0);
	[] ->
	    list_config(burner_config(), 
			{error,"2,missing alias"}),
	    erlang:halt(0);
	_ ->
	    Options = parse_query(string_to_unicode(Query)),
	    %%file:write_file(?TMP1, io_lib:format("~p\n", [Options])),
	    run(Options)
    end;
main(Query) ->
    Options = parse_query(string_to_unicode(Query)),
    %%file:write_file(?TMP2, io_lib:format("~p\n", [Options])),
    run(Options).

run(Options) ->
    Config = load_config(burner_config()),
    case proplists:get_value("action",Options) of
	"list" ->
	    list_table(standard_io, ok, Config),
	    erlang:halt(0);
	"add" ->
	    case proplists:get_value("alias", Options) of
		undefined ->
		    list_config(burner_config(),
				{error,"3,missing alias"});
		Alias ->
		    case find_alias(Alias, Config) of
			false ->
			    Entry = set_options(Options, 
						#{alias => Alias,
						  date => {date(),time()},
						  block => false,
						  site => "www.rogvall.se",
						  password => "",
						  comment => ""}),
			    Config1 = Config ++ [Entry],
			    ok = save_config(burner_config(), Config1),
			    list_config(burner_config(), ok),
			    erlang:halt(0);
			_Entry ->
			    list_config(burner_config(), 
					{error,"alias already exists"})
		    end
	    end;
	"del" ->
	    case proplists:get_value("alias", Options) of
		undefined ->
		    list_config(burner_config(),
				{error,"4,missing alias"});
		Alias ->
		    case find_alias(Alias, Config) of
			false ->
			    list_config(burner_config(),
					{error,"alias do not exist"});
			_ ->
			    Config1 = delete_alias(Alias, Config),
			    ok = save_config(burner_config(), Config1),
			    list_config(burner_config(), ok)
		    end
	    end;
	"mod" ->
	    case proplists:get_value("alias", Options) of
		undefined ->
		    list_config(burner_config(),
				{error,"5,missing alias"});
		Alias ->
		    case find_alias(Alias, Config) of
			false ->
			    list_config(burner_config(),
					{error,"alias do not exist"});
			_ ->
			    Config1 = modify_alias(Alias, Options, Config),
			    Status = save_config(burner_config(), Config1),
			    list_config(burner_config(), Status)
		    end
	    end;
	_ ->
	    list_config(burner_config(),
			{error,"unknown action"})
    end,
    erlang:halt(0).


burner_config() ->
    case os:type() of
	{unix, linux} ->
	    ?BURNER_CONFIG_LINUX;
	{unix, darwin} ->
	    ?BURNER_CONFIG_MACOS
    end.

string_to_unicode(Arg) ->
    BinArg = list_to_binary(Arg),
    case unicode:characters_to_binary(BinArg, utf8) of
	{error,_,_} ->
	    unicode:characters_to_list(BinArg, latin1);
	Utf8 ->
	    binary_to_list(Utf8)
    end.


%% add/set options
set_options([{"block","true"}|Options], Entry) ->
    set_options(Options, Entry#{ block=>true });
set_options([{"block","false"}|Options], Entry) ->
    set_options(Options, Entry#{ block=>false });
set_options([{"site",Domain}|Options], Entry) ->
    set_options(Options, Entry#{ site=>Domain });
set_options([{"comment",Comment}|Options], Entry) ->
    set_options(Options, Entry#{ comment=>Comment });
set_options([{"password",Password}|Options], Entry) ->
    set_options(Options, Entry#{ password=>Password });
set_options([_|Options], Entry) -> set_options(Options, Entry);
set_options([], Entry) ->
    Entry.


%% delete 
find_alias(Alias, [Entry|List]) when is_map(Entry) ->
    case maps:get(alias, Entry, undefined) of
	Alias -> Entry;
	_ ->
	    find_alias(Alias, List)
    end;
find_alias(Alias, [_Entry|List]) ->
    find_alias(Alias, List);
find_alias(_Alias, []) ->
    false.



%% delete 
delete_alias(Alias, [Entry|List]) when is_map(Entry) ->
    case maps:get(alias, Entry, undefined) of
	Alias -> List;  %% done
	_ -> [Entry|delete_alias(Alias, List)]
    end;
delete_alias(Alias, [Entry|List]) ->
    [Entry|delete_alias(Alias, List)];
delete_alias(_Alias, []) ->
    [].

%% modify
modify_alias(Alias, Options, [Entry|List]) when is_map(Entry) ->
    case maps:get(alias, Entry, undefined) of
	Alias -> 
	    [set_options(Options, Entry) | List];
	_ ->
	    [Entry|modify_alias(Alias, Options, List)]
    end;
modify_alias(Alias, Options, [Entry|List]) ->
    [Entry|modify_alias(Alias, Options, List)];
modify_alias(_Alias, _Options, []) ->
    [].

list_config(Filename, Status) ->
    Config = load_config(Filename),
    list_table(standard_io, Status, Config).

list_table(Fd, Status, Config) ->
    io:format(Fd, "Content-type: text/html\r\n\r\n", []),
    io:format(Fd, "<script id=\"ssi-data\" type=\"application/json\">\n",[]),
    io:format(Fd, "  [\n", []),
    list_rows(Fd, "    ", Config),
    io:format(Fd, "  ]\n", []),
    io:format(Fd, "</script>\n", []),
    io:format(Fd, "<script id=\"ssi-error\" type=\"application/json\">\n",[]),
    case Status of
	ok ->
	    io:format(Fd, "  {\"status\":\"ok\"}\n", []);
	{error,Reason} ->
	    io:format(Fd, "  {\"status\":\"error\",\"message\":~tp}\n", 
		      [to_string(Reason)])
    end,
    io:format(Fd, "</script>\n", []).

list_rows(Fd, Indent, Config) ->    
    Config1 = [C || C <- Config, is_map(C)],
    list_rows_(Fd, Indent, Config1).

list_rows_(Fd, Indent, []) ->
    ok;
list_rows_(Fd, Indent, [E]) ->
    io:format(Fd, Indent++"~ts\n", [format_entry(E)]);
list_rows_(Fd, Indent, [E|Es]) ->
    io:format(Fd, Indent++"~ts,\n", [format_entry(E)]),
    list_rows_(Fd, Indent, Es).

load_config(Filename) ->
    case consult(Filename) of
	{ok, Config} ->
	    Config;
	{error, Error} ->
	    io:format(standard_error, "error: ~p\n", [Error]),
	    erlang:halt(1)
    end.

save_config(Filename, Config) ->
    case file:open(Filename, [write]) of
	{ok, Fd} ->
	    io:format(Fd, "%% -*- erlang -*-\n", []),
	    lists:foreach(
	      fun(Entry) ->
		      io:format(Fd, "~p.\n", [Entry])
	      end, Config),
	    file:close(Fd);
	{error, _} ->
	    error
    end.

%% format entry as json
format_entry(Entry) ->
    %% translate internal date/string to json acceptable format
    Name = maps:get(alias, Entry, ""),
    Alias = to_utf8(Name),
    Pass = maps:get(password, Entry, ""),
    Password = to_binary(Pass),    
    Com = maps:get(comment, Entry, ""),
    Comment = to_utf8(Com),
    {{YYYY,MM,DD},{H,M,_S}} = maps:get(date, Entry),
    Date = to_binary(io_lib:format("~04w~.2.0w~.2.0w", [YYYY,MM,DD])),
    Time = to_binary(io_lib:format("~.2.0w:~.2.0w", [H,M])),
    Dom = maps:get(site, Entry, ""),

    Site = to_binary(Dom),
    json:encode(Entry#{ alias=>Alias, date=>Date, time=>Time,
			site=>Site, password=>Password,comment=>Comment}).

to_binary(Value) when is_atom(Value) ->
    atom_to_binary(Value);
to_binary(Value) when is_list(Value) ->
    list_to_binary(Value);
to_binary(Value) when is_binary(Value) ->
    Value.

to_utf8(Value) when is_atom(Value) ->
    atom_to_binary(Value, utf8);
to_utf8(Value) when is_list(Value) ->
    unicode:characters_to_binary(Value, utf8);
to_utf8(Value) when is_binary(Value) ->
    Value.

to_string(Value) when is_atom(Value) ->
    atom_to_list(Value);
to_string(Value) when is_list(Value) ->
    Value;
to_string(Value) when is_binary(Value) ->
    binary_to_list(Value).

consult(File) ->
    case file:read_file(File) of
	{ok,Bin} ->
	    Cs = case unicode:characters_to_list(Bin, utf8) of
		     {error, _, _} ->
			 binary_to_list(Bin);
		     List -> List
		 end,
	    case trim(Cs) of
		[] ->
		    {ok,[]};
		Cs1 ->
		    case erl_scan:string(Cs1) of
			{ok, Ts, _} ->
			    try parse_term_list(Ts) of
				{ok, Es}  -> {ok, Es}
			    catch
				error:Reason ->
				    {error, Reason}
			    end;
			{error,Error,_} ->
			    {error, Error}
		    end
	    end;
	Error ->
	    Error
    end.

parse_term_list(Ts) ->
    parse_term_list(Ts,[]).
parse_term_list([],Acc) ->
    {ok,lists:reverse(Acc)};
parse_term_list(Ts,Acc) ->
    {Ts1, Ts2} = split_term(Ts),
    case erl_parse:parse_term(Ts1) of
	{ok, Term} ->
	    parse_term_list(Ts2, [Term | Acc]);
	Error ->
	    Error
    end.

split_term(Ts) ->
    split_term(Ts,[]).

split_term([T={dot,_Ln}|Ts],Acc) ->
    {lists:reverse([T|Acc]), Ts};
split_term([T|Ts], Acc) ->
    split_term(Ts, [T|Acc]).

trim([$\s|Cs]) -> trim(Cs);
trim([$\t|Cs]) -> trim(Cs);
trim(Cs) -> Cs.

parse_query(Cs) ->
    parse_seq(Cs).

parse_seq(Cs) ->
    [case string:tokens(Kv,"=") of
	 [Key0,Value0] ->
	     Key1 = url_decode(Key0),
	     Value1 = url_decode(Value0),
	     try list_to_integer(string:trim(Value1)) of
		 Value -> {Key1, Value}
	     catch
		 error:_ -> {Key1, Value1}
	     end;
	 [Key0] ->
	     {url_decode(Key0),true}
     end || Kv <- string:tokens(Cs, "&")].

url_decode([$%,C1,C2|T]) ->
    C = list_to_integer([C1,C2], 16),
    [C | url_decode(T)];
url_decode([$+|T]) -> [$\s|url_decode(T)];
url_decode([C|T]) -> [C|url_decode(T)];
url_decode([]) -> [].
