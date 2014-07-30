# coding: utf-8

# BlackSmith mark.2
# exp_name = "allweb" # /code.py v.x28
#  Id: 26~27c
#  Code © (2011-2013) by WitcherGeralt [alkorgun@gmail.com]
import requests
from lxml import html

class expansion_temp(expansion):
    def __init__(self, name):
        expansion.__init__(self, name)

    UserAgents = UserAgents

    import htmlentitydefs, json

    UserAgent = ("User-Agent", "%s/%s" % (ProdName[:10], CapsVer))

    UserAgent_Moz = (UserAgent[0],
                     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36".format(
                         UserAgents.get(DefLANG, "en-US")))

    Web.Opener.addheaders = [UserAgent_Moz]

    edefs = dict()

    for Name, Numb in htmlentitydefs.name2codepoint.iteritems():
        edefs[Name] = unichr(Numb)

    del Name, Numb

    edefs["&apos;"] = unichr(39)

    TagsDesc = {
    "<br>": chr(10),
    "<br />": chr(10)
    }

    compile_st = compile__("<[^<>]+?>")
    compile_ehtmls = compile__("&(#?[xX]?(?:[0-9a-fA-F]+|\w{1,8}));")

    def sub_ehtmls(self, data):
        if data.count("&"):

            def e_sb(co):
                co = co.group(1)
                if co.startswith("#"):
                    if chr(120) == co[1].lower():
                        Char, c06 = co[2:], 16
                    else:
                        Char, c06 = co[1:], 10
                    try:
                        Numb = int(Char, c06)
                        assert (-1 < Numb < 65535)
                        Char = unichr(Numb)
                    except Exception:
                        Char = self.edefs.get(Char, "&%s;" % co)
                else:
                    Char = self.edefs.get(co, "&%s;" % co)
                return Char

            data = self.compile_ehtmls.sub(e_sb, data)
        return data

    def decodeHTML(self, data):
        data = sub_desc(data, self.TagsDesc)
        data = self.compile_st.sub("", data)
        data = self.sub_ehtmls(data)
        return data.strip()

    def command_jc(self, stype, source, body, disp):
        if Chats.has_key(source[1]):
            if body:
                cName = body.lower()
                if cName.count("@conf"):
                    cName = (cName.split("@conf"))[0]
            else:
                cName = (source[1].split("@conf"))[0]
            Opener = Web("http://jc.jabber.ru/search.html?", [("search", cName.encode("utf-8"))])
            try:
                data = Opener.get_page(self.UserAgent)
            except Web.Two.HTTPError as exc:
                answer = str(exc)
            except Exception:
                answer = self.AnsBase[0]
            else:
                data = data.decode("utf-8")
                comp = compile__("<li>((?:.|\s)+?)</li>", 16)
                list = comp.findall(data)
                if list:
                    ls = []
                    for numb, line in enumerate(list, 1):
                        line = line.strip()
                        ls.append("%d) %s" % (numb, line))
                    answer = chr(10) + self.decodeHTML(str.join(chr(10) * 2, ls))
                else:
                    answer = self.AnsBase[5]
        else:
            answer = AnsBase[0]
        Answer(answer, stype, source, disp)

    gCache = []

    sMark = 1
    tMark = 2

    def command_google(self, stype, source, body, disp):
        if body:
            if (chr(42) != body):
                Opener = Web("http://ajax.googleapis.com/ajax/services/search/web?",
                             [("v", "1.0"), ("q", body.encode("utf-8"))])
                try:
                    data = Opener.get_page(self.UserAgent)
                except Web.Two.HTTPError as exc:
                    answer = str(exc)
                except Exception:
                    answer = self.AnsBase[0]
                else:
                    try:
                        data = self.json.loads(data)
                    except Exception:
                        answer = self.AnsBase[1]
                    else:
                        try:
                            list = data["responseData"]["results"]
                            desc = list.pop(0)
                        except (TypeError, LookupError):
                            answer = self.AnsBase[5]
                        else:
                            ls = []
                            ls.append(desc.get("title", ""))
                            ls.append(desc.get("content", ""))
                            ls.append(desc.get("unescapedUrl", ""))
                            answer = self.decodeHTML(str.join(chr(10), ls))
                            if list:
                                source_ = get_source(source[1], source[2])
                                if source_:
                                    for ls in self.gCache:
                                        if ls[:2] == (source_, self.sMark):
                                            self.gCache.pop(self.gCache.index(ls))
                                            break
                                    Numb = (len(Clients.keys()) * 8)
                                    while len(self.gCache) >= Numb:
                                        self.gCache.pop(0)
                                    self.gCache.append((source_, self.sMark, list))
                                    answer += self.AnsBase[4] % len(list)
            else:
                source_ = get_source(source[1], source[2])
                if source_:
                    list = []
                    for ls in self.gCache:
                        if ls[:2] == (source_, self.sMark):
                            list = self.gCache.pop(self.gCache.index(ls))[2]
                            break
                    if list:
                        desc = list.pop(0)
                        ls = []
                        ls.append(desc.get("title", ""))
                        ls.append(desc.get("content", ""))
                        ls.append(desc.get("unescapedUrl", ""))
                        answer = self.decodeHTML(str.join(chr(10), ls))
                        if list:
                            self.gCache.append((source_, self.sMark, list))
                            answer += self.AnsBase[4] % len(list)
                    else:
                        answer = self.AnsBase[2]
                else:
                    answer = self.AnsBase[3]
        else:
            answer = AnsBase[1]
        Answer(answer, stype, source, disp)

    LangMap = LangMap

    def command_google_translate(self, stype, source, body, disp):
        if body:
            if (chr(42) != body):
                body = body.split(None, 2)
                if len(body) == 3:
                    lang0, langX, body = body
                    if langX in self.LangMap and (lang0 in self.LangMap or lang0 == "auto"):
                        desc = (("client", "bs-2"),
                                ("sl", lang0),
                                ("tl", langX),
                                ("text", body.encode("utf-8")))
                        Opener = Web("http://translate.google.com/translate_a/t?", desc,
                                     headers={"Accept-Charset": "utf-8"})
                        try:
                            data = Opener.get_page(self.UserAgent_Moz)
                        except Web.Two.HTTPError as exc:
                            answer = str(exc)
                        except Exception:
                            answer = self.AnsBase[0]
                        else:
                            try:
                                data = self.json.loads(data)
                            except Exception:
                                answer = self.AnsBase[1]
                            else:
                                try:
                                    body = data["sentences"][0]["trans"]
                                except (TypeError, LookupError):
                                    answer = self.AnsBase[1]
                                else:
                                    if lang0 == "auto":
                                        try:
                                            lang0 = data["src"]
                                        except KeyError:
                                            pass
                                    answer = "%s -> %s:\n%s" % (lang0, langX, body)
                                    try:
                                        list = data["dict"][0]["terms"]
                                    except LookupError:
                                        pass
                                    else:
                                        source_ = get_source(source[1], source[2])
                                        if source_:
                                            if body in list:
                                                list.pop(list.index(body))
                                            if list:
                                                for ls in self.gCache:
                                                    if ls[:2] == (source_, self.tMark):
                                                        self.gCache.pop(self.gCache.index(ls))
                                                        break
                                                Numb = (len(Clients.keys()) * 8)
                                                while len(self.gCache) >= Numb:
                                                    self.gCache.pop(0)
                                                self.gCache.append((source_, self.tMark, list))
                                                answer += self.AnsBase[7] % len(list)
                    else:
                        answer = self.AnsBase[6]
                else:
                    answer = AnsBase[2]
            else:
                source_ = get_source(source[1], source[2])
                if source_:
                    list = []
                    for ls in self.gCache:
                        if ls[:2] == (source_, self.tMark):
                            list = self.gCache.pop(self.gCache.index(ls))[2]
                            break
                    if list:
                        answer = self.decodeHTML(list.pop(0))
                        if list:
                            self.gCache.append((source_, self.tMark, list))
                            answer += self.AnsBase[7] % len(list)
                    else:
                        answer = self.AnsBase[2]
                else:
                    answer = self.AnsBase[3]
        else:
            answer = self.AnsBase[8] + str.join(chr(10), ["%s - %s" % (k, l) for k, l in sorted(self.LangMap.items())])
            if stype == sBase[1]:
                Message(source[0], answer, disp)
                answer = AnsBase[11]
        Answer(answer, stype, source, disp)

    kinoHeaders = {
    "Host": "m.kinopoisk.ru",
    "Accept": "text/html",
    "Accept-Charset": "cp1251",
    "Accept-Language": "ru"
    }

    C3oP = "СЗоР"

    def command_kino(self, stype, source, body, disp):
        if body:
            ls = body.split()
            c1st = (ls.pop(0)).lower()
            if c1st in ("top250", "топ250".decode("utf-8")):
                if ls:
                    limit = apply(int, (ls.pop(0),))
                    if limit <= 5:
                        limit = 5
                else:
                    limit = None
                kinoHeaders = self.kinoHeaders.copy()
                kinoHeaders["Host"] = "www.kinopoisk.ru"
                Opener = Web("http://www.kinopoisk.ru/level/20/", headers=kinoHeaders)
                try:
                    data = Opener.get_page(self.UserAgent_Moz)
                except Web.Two.HTTPError as exc:
                    answer = str(exc)
                except Exception:
                    answer = self.AnsBase[0]
                else:
                    data = data.decode("cp1251")
                    list = get_text(data, "<tr height=25>", "</table>")
                    if list:
                        comp = compile__('<a href="/film/\d+?/" class="all">(.+?)</a>(?:.|\s)+' \
                                         '?<a href="/film/\d+?/votes/" class="continue">(.+?)</a> <span.*?>(.+?)</span>',
                                         16)
                        list = comp.findall(list)
                    if list:
                        ls = ["\n[#] [Name, Year] [Rating] (Votes)"]
                        for Number, (Name, Numb, Count) in enumerate(list, 1):
                            ls.append(
                                "%d) %s - %s %s" % (Number, self.sub_ehtmls(Name), Numb, sub_desc(Count, ["&nbsp;"])))
                            if limit and limit <= Number:
                                break
                        if not limit or limit > 25:
                            if stype == sBase[1]:
                                Answer(AnsBase[11], stype, source, disp)
                            Top250 = str.join(chr(10), ls)
                            Message(source[0], Top250, disp)
                        else:
                            answer = str.join(chr(10), ls)
                    elif data.count(self.C3oP):
                        answer = self.AnsBase[-1]
                    else:
                        answer = self.AnsBase[1]
            elif isNumber(body):
                Opener = Web("http://m.kinopoisk.ru/movie/%d" % int(body), headers=self.kinoHeaders.copy())
                try:
                    data = Opener.get_page(self.UserAgent_Moz)
                except Web.Two.HTTPError as exc:
                    answer = str(exc)
                except Exception:
                    answer = self.AnsBase[0]
                else:
                    data = data.decode("cp1251")
                    rslt = get_text(data, "<p class=\"title\">", "</div>")
                    if rslt:
                        rslt = self.decodeHTML(rslt)
                        ls = ["\->"]
                        for line in rslt.splitlines():
                            line = line.strip()
                            if line:
                                if line[0].islower():
                                    line = "{1}{0}".format(line[1:], line[0].upper())
                                ls.append(line)
                        answer = str.join(chr(10), ls)
                    elif data.count(self.C3oP):
                        answer = self.AnsBase[-1]
                    else:
                        answer = self.AnsBase[5]
            else:
                body = (body if chr(42) != c1st else body[2:].strip())
                if body:
                    body = body.encode("cp1251")
                    Opener = Web("http://m.kinopoisk.ru/search/%s" % Web.One.quote_plus(body),
                                 headers=self.kinoHeaders.copy())
                    try:
                        data = Opener.get_page(self.UserAgent_Moz)
                    except Web.Two.HTTPError as exc:
                        answer = str(exc)
                    except Exception:
                        answer = self.AnsBase[0]
                    else:
                        data = data.decode("cp1251")
                        comp = compile__("<a href=\"http://m.kinopoisk.ru/movie/(\d+?)/\">(.+?)</a>")
                        list = comp.findall(data)
                        if list:
                            ls = ["\n[#] [Name, Year] (#id)"]
                            for Number, (Numb, Name) in enumerate(list, 1):
                                ls.append("%d) %s (#%s)" % (Number, self.sub_ehtmls(Name), Numb))
                            answer = str.join(chr(10), ls)
                        elif data.count(self.C3oP):
                            answer = self.AnsBase[-1]
                        else:
                            answer = self.AnsBase[5]
                else:
                    answer = AnsBase[2]
        else:
            answer = AnsBase[1]
        if locals().has_key(sBase[6]):
            Answer(answer, stype, source, disp)

    IMDbHeaders = {"Accept-Language": "%s,en" % UserAgents.get(DefLANG, "en-US")}

    IMDbRequest = {  # imdbapi.org
                     "type": "json",
                     #		"id": "tt", # get info by ID
                     #		"q": "any title", # for the search
                     #		"limit": str(choice(range(1, 11))), # for the search
                     "plot": "none",  # or "simple" or "full"
                     "episode": "0",  # or "1"
                     "lang": UserAgents.get(DefLANG, "en-US"),
                     "aka": "simple",  # or "full"
                     "release": "simple",  # or "full"
    }

    def command_imdb(self, stype, source, body, disp):
        if body:
            ls = body.split()
            c1st = (ls.pop(0)).lower()
            if c1st in ("top250", "топ250".decode("utf-8")):
                if ls:
                    limit = apply(int, (ls.pop(0),))
                    if limit <= 5:
                        limit = 5
                else:
                    limit = None
                Opener = Web("http://m.imdb.com/chart/top_json", headers=self.IMDbHeaders)
                try:
                    data = Opener.get_page(self.UserAgent_Moz)
                except Web.Two.HTTPError as exc:
                    answer = str(exc)
                except Exception:
                    answer = self.AnsBase[0]
                else:
                    try:
                        data = self.json.loads(data)
                    except Exception:
                        answer = self.AnsBase[1]
                    else:
                        try:
                            data = data["list"]
                        except (TypeError, LookupError):
                            answer = self.AnsBase[1]
                        else:
                            ls = ["\n[#] [Name, Year] [Rating] (Votes)"]
                            comp = compile__("([\d\.,]+).*\s([\d\.,]+)")
                            try:

                                assert isinstance(data, list)

                                for Number, desc in enumerate(data, 1):
                                    Name = desc["title"]
                                    Year = desc["extra"]
                                    Numb, Count = comp.search(desc["detail"]).groups()
                                    ls.append("%s) %s %s - %s (%s)" % (Number, Name, Year, Numb, Count))
                                    if limit and limit <= Number:
                                        break
                            except (AssertionError, TypeError, LookupError):
                                answer = self.AnsBase[5]
                            else:
                                if not limit or limit > 25:
                                    if stype == sBase[1]:
                                        Answer(AnsBase[11], stype, source, disp)
                                    Top250 = str.join(chr(10), ls)
                                    Message(source[0], Top250, disp)
                                else:
                                    answer = str.join(chr(10), ls)
            elif isNumber(body):
                IMDbRequest = self.IMDbRequest.copy()
                IMDbRequest["id"] = ("tt" + body)
                IMDbRequest["plot"] = "full"
                Opener = Web("http://imdbapi.org/?", IMDbRequest.items())
                try:
                    data = Opener.get_page(self.UserAgent_Moz)
                except Web.Two.HTTPError as exc:
                    answer = str(exc)
                except Exception:
                    answer = self.AnsBase[0]
                else:
                    try:
                        data = self.json.loads(data)
                    except Exception:
                        answer = self.AnsBase[1]
                    else:
                        ls = ["\->"]
                        try:

                            assert isinstance(data, dict)

                            ls.append("%s, %s, %s." % (
                            data["title"], data["year"], str.join(chr(32), data.get("runtime", ("??",)))))
                            ls.append(", ".join(data["genres"]))
                            ls.append(", ".join(data["country"]))
                            temp = data.get("directors")
                            if temp:
                                ls.append("Directors: " + ", ".join(temp[:3]))
                            temp = data.get("writers")
                            if temp:
                                ls.append("Writers: " + ", ".join(temp[:3]))
                            temp = data.get("actors")
                            if temp:
                                ls.append("Stars: " + ", ".join(temp[:5]))
                            temp = data.get("plot") or data.get("plot_simple")
                            if temp:
                                ls.append(unichr(171) + temp + unichr(187))
                            temp = data.get("rating")
                            if temp:
                                ls.append("IMDb rating: %s (%s)" % (temp, data.get("rating_count", 0)))
                        except (AssertionError, TypeError, LookupError):
                            answer = self.AnsBase[5]
                        else:
                            answer = self.sub_ehtmls(str.join(chr(10), ls))
            else:
                body = (body if chr(42) != c1st else body[2:].strip())
                if body:
                    body = body.encode("utf-8")
                    IMDbRequest = self.IMDbRequest.copy()
                    IMDbRequest["q"] = body
                    IMDbRequest["limit"] = "10"
                    Opener = Web("http://imdbapi.org/?", IMDbRequest.items())
                    try:
                        data = Opener.get_page(self.UserAgent_Moz)
                    except Web.Two.HTTPError as exc:
                        answer = str(exc)
                    except Exception:
                        answer = self.AnsBase[0]
                    else:
                        try:
                            data = self.json.loads(data)
                        except Exception:
                            answer = self.AnsBase[1]
                        else:
                            try:

                                assert isinstance(data, list)

                                data = sorted([(desc.get("rating"),
                                                desc["title"],
                                                desc["year"],
                                                desc["imdb_id"][2:]) for desc in data], reverse=True)
                            except (AssertionError, TypeError, LookupError):
                                answer = self.AnsBase[5]
                            else:
                                ls = ["\n[#] [Name, Year] (#id)"]
                                for Number, (Numb, Name, Year, ID) in enumerate(data, 1):
                                    ls.append("%d) %s, %s (#%s)" % (Number, Name, Year, ID))
                                answer = self.sub_ehtmls(str.join(chr(10), ls))
                else:
                    answer = AnsBase[2]
        else:
            answer = AnsBase[1]
        if locals().has_key(sBase[6]):
            Answer(answer, stype, source, disp)

    def command_python(self, stype, source, body, disp):

        def parsing_lxml_path(text, path):
            tree = html.fromstring(text)
            texts = tree.xpath(path)
            texts = [x.text for x in texts]
            #r.close()
            return texts

        def get_news():
            url = 'http://blog.python.org/'
            try:
                t = requests.get(url, verify=False)
                l = parsing_lxml_path(t.text, '//h2[@class="date-header"]/span')
                pl = parsing_lxml_path(t.text, '//h3[@class="post-title entry-title"]/a')
                #l = [x.tostring() for x in l]
                return list(set(zip(l, pl)))
            except requests.ConnectionError as e:
                pass
        answer = '\n\n'.join(['\n'.join(x) for x in get_news()])
        Answer(answer, stype, source, disp)

    def command_url_shorten(self, stype, source, body, disp):
        if body:
            Opener = Web("http://is.gd/create.php?", [("format", "json"), ("url", body.encode("utf-8"))])
            try:
                data = Opener.get_page(self.UserAgent)
            except Web.Two.HTTPError as exc:
                answer = str(exc)
            except Exception:
                answer = self.AnsBase[0]
            else:
                try:
                    data = self.json.loads(data)
                except Exception:
                    answer = self.AnsBase[1]
                else:
                    try:
                        answer = data["shorturl"]
                    except KeyError:
                        try:
                            answer = data["errormessage"]
                        except KeyError:
                            answer = self.AnsBase[1]
        else:
            answer = AnsBase[1]
        Answer(answer, stype, source, disp)

    downloadLock = ithr.allocate_lock()

    def download_process(self, info, blockNumb, blockSize, size, fb):
        if not blockNumb:
            Print("\n")
            Print(str(info), color3)
        elif size >= blockSize:
            fb[3] += blockSize
            if not fb[4]:
                fb[4] = (size / 100)
                if fb[4] in (0, 1):
                    fb[4] = 2
                else:
                    residue = fb[4] % blockSize
                    if fb[4] == residue:
                        fb[4] = 2
                        while fb[4] < residue:
                            fb[4] *= 2
                    elif residue:
                        fb[4] -= residue
            if fb[3] >= size:
                Print("Done.", color3)
            elif not fb[3] % fb[4]:
                Pcts = fb[3] / fb[4]
                if Pcts == 100:
                    Pcts = 99.95
                Print("loaded - {0}%".format(Pcts), color4)
                Time = time.time()
                if Time - fb[1] >= 30:
                    fb[1] = Time
                    Message(fb[0], self.AnsBase[9].format(Pcts), fb[2])

    def command_download(self, stype, source, body, disp):
        if body:
            if not self.downloadLock.locked():
                with self.downloadLock:
                    body = body.split()
                    if len(body) == 1:
                        link = body.pop()
                        folder = None
                        filename = None
                    elif len(body) == 2:
                        link, folder = body
                        filename = None
                    else:
                        link, folder, filename = body[:3]
                    if not enough_access(source[1], source[2], 8):
                        folder = "Downloads"
                    if filename:
                        filename = os.path.basename(filename.rstrip("\\/"))
                    if folder:
                        folder = os.path.normpath(folder)
                        if AsciiSys:
                            folder = folder.encode("utf-8")
                        if not os.path.isdir(folder):
                            try:
                                os.makedirs(folder)
                            except Exception:
                                link = None
                        if AsciiSys:
                            folder = folder.decode("utf-8")
                    if link:
                        Message(source[0], self.AnsBase[10], disp)
                        Opener = Web(link)
                        try:
                            data = Opener.download(filename, folder, self.download_process,
                                                   [source[0], time.time(), disp, 0, 0], self.UserAgent)
                        except Web.Two.HTTPError as exc:
                            answer = str(exc)
                        except SelfExc as exc:
                            answer = "Error! %s." % exc[0].capitalize()
                        except Exception:
                            answer = self.AnsBase[0]
                        else:
                            answer = "Done.\nPath: %s\nSize: %s" % (data[0], Size2Text(data[2]))
                    else:
                        answer = AnsBase[2]
            else:
                answer = self.AnsBase[11]
        else:
            answer = AnsBase[1]
        Answer(answer, stype, source, disp)

    PasteLangs = PasteLangs

    def command_paste(self, stype, source, body, disp):
        if body:
            args = body.split(None, 1)
            arg0 = (args.pop(0)).lower()
            if arg0 in self.PasteLangs:
                if args:
                    body = args.pop()
                else:
                    body = None
                    answer = AnsBase[2]
            else:
                arg0 = "text"
            if body:
                Opener = Web("http://paste.ubuntu.com/",
                             data=Web.encode({"poster": ProdName, "syntax": arg0, "content": body.encode("utf-8")}))
                try:
                    fp = Opener.open(self.UserAgent)
                    answer = fp.url
                    fp.close()
                except Web.Two.HTTPError as exc:
                    answer = str(exc)
                except Exception:
                    answer = self.AnsBase[0]
        else:
            answer = self.AnsBase[8] + str.join(chr(10),
                                                ["%s - %s" % (k, l) for k, l in sorted(self.PasteLangs.items())])
            if stype == sBase[1]:
                Message(source[0], answer, disp)
                answer = AnsBase[11]
        Answer(answer, stype, source, disp)

    if DefLANG in ("RU", "UA"):

        def command_chuck(self, stype, source, body, disp):
            if body and isNumber(body):
                Opener = Web("http://chucknorrisfacts.ru/quote/%d" % int(body))
            else:
                Opener = Web("http://chucknorrisfacts.ru/random")
            try:
                data = Opener.get_page(self.UserAgent)
            except Web.Two.HTTPError as exc:
                answer = str(exc)
            except Exception:
                answer = self.AnsBase[0]
            else:
                data = data.decode("cp1251")
                comp = compile__("<a href=/quote/(\d+?)>.+?<blockquote>(.+?)</blockquote>", 16)
                data = comp.search(data)
                if data:
                    answer = self.decodeHTML("#%s\n%s" % data.groups())
                else:
                    answer = self.AnsBase[1]
            Answer(answer, stype, source, disp)

        def command_bash(self, stype, source, body, disp):
            if body and isNumber(body):
                Opener = Web("http://bash.im/quote/%d" % int(body))
            else:
                Opener = Web("http://bash.im/random")
            try:
                data = Opener.get_page(self.UserAgent)
            except Web.Two.HTTPError as exc:
                answer = str(exc)
            except Exception:
                answer = self.AnsBase[0]
            else:
                data = data.decode("cp1251")
                comp = compile__(
                    '<span id="v\d+?" class="rating">(.+?)</span>(?:.|\s)+?<a href="/quote/\d+?" class="id">#(\d+?)</a>\s*?</div>\s+?<div class="text">(.+?)</div>',
                    16)
                data = comp.search(data)
                if data:
                    answer = self.decodeHTML("#{1} +[{0}]-\n{2}".format(*data.groups()))
                else:
                    answer = self.AnsBase[1]
            Answer(answer, stype, source, disp)

    else:

        def command_chuck(self, stype, source, body, disp):
            Opener = Web("http://www.chucknorrisfacts.com/all-chuck-norris-facts?page=%d" % randrange(
                974))  # 04:12 09.11.2012 by UTC number of pages was 974
            try:
                data = Opener.get_page(self.UserAgent)
            except Web.Two.HTTPError as exc:
                answer = str(exc)
            except Exception:
                answer = self.AnsBase[0]
            else:
                data = data.decode("utf-8")
                comp = compile__("<span class=\"field-content\"><a.*?>(.+?)</a></span>", 16)
                list = comp.findall(data)
                if list:
                    answer = self.decodeHTML(choice(list))
                else:
                    answer = self.AnsBase[1]
            Answer(answer, stype, source, disp)

        def command_bash(self, stype, source, body, disp):
            if body and isNumber(body):
                Opener = Web("http://bash.org/?%d" % int(body))
            else:
                Opener = Web("http://bash.org/?random")
            try:
                data = Opener.get_page(self.UserAgent)
            except Web.Two.HTTPError as exc:
                answer = str(exc)
            except Exception:
                answer = self.AnsBase[0]
            else:
                data = data.decode("iso-8859-1")
                comp = compile__(
                    '<b>#(\d+?)</b></a>\s<a.*?>\+</a>\((.+?)\)<a.*?>-</a>\s<a.*?>\[X\]</a></p><p class="qt">(.+?)</p>',
                    16)
                data = comp.search(data)
                if data:
                    answer = self.decodeHTML("#%s +[%s]-\n%s" % data.groups())
                else:
                    answer = self.AnsBase[1]
            Answer(answer, stype, source, disp)

    def command_currency(self, stype, source, body, disp):
        if body:
            ls = body.split()
            Code = (ls.pop(0)).lower()
            if Code in ("code", "аббревиатура".decode("utf-8")):
                if ls:
                    Code = (ls.pop(0)).upper()
                    if Code in self.CurrencyDesc:
                        answer = self.CurrencyDesc[Code].decode("utf-8")
                    else:
                        answer = self.AnsBase[1]
                else:
                    answer = AnsBase[2]
            elif Code in ("list", "список".decode("utf-8")):
                if stype == sBase[1]:
                    Answer(AnsBase[11], stype, source, disp)
                Curls = ["\->"] + ["%s: %s" % desc for desc in sorted(self.CurrencyDesc.items())]
                Message(source[0], str.join(chr(10), Curls), disp)
            elif Code in ("calc", "перевести".decode("utf-8")):
                if len(ls) >= 2:
                    Number = ls.pop(0)
                    if isNumber(Number) and ls[0].isalpha():
                        Number = int(Number)
                        Code = (ls.pop(0)).upper()
                        if (Code == "RUB"):
                            answer = "%d %s" % (Number, Code)
                        elif Code in self.CurrencyDesc:
                            Opener = Web("http://www.cbr.ru/scripts/XML_daily.asp")
                            try:
                                data = Opener.get_page(self.UserAgent)
                            except Web.Two.HTTPError as exc:
                                answer = str(exc)
                            except Exception:
                                answer = self.AnsBase[0]
                            else:
                                data = data.decode("cp1251")
                                comp = compile__(
                                    "<CharCode>%s</CharCode>\s+?<Nominal>(.+?)</Nominal>\s+?<Name>.+?</Name>\s+?<Value>(.+?)</Value>" % (
                                    Code), 16)
                                data = comp.search(data)
                                if data:
                                    No, Numb = data.groups()
                                    Numb = Numb.replace(chr(44), chr(46))
                                    No = No.replace(chr(44), chr(46))
                                    try:
                                        Numb = (Number * (float(Numb) / float(No)))
                                    except Exception:
                                        answer = AnsBase[7]
                                    else:
                                        answer = "%.2f RUB" % (Numb)
                                else:
                                    answer = self.AnsBase[1]
                        else:
                            answer = AnsBase[2]
                    else:
                        answer = AnsBase[2]
                else:
                    answer = AnsBase[2]
            elif (Code != "rub") and Code.isalpha():
                Code = Code.upper()
                if Code in self.CurrencyDesc:
                    Opener = Web("http://www.cbr.ru/scripts/XML_daily.asp")
                    try:
                        data = Opener.get_page(self.UserAgent)
                    except Web.Two.HTTPError as exc:
                        answer = str(exc)
                    except Exception:
                        answer = self.AnsBase[0]
                    else:
                        data = data.decode("cp1251")
                        comp = compile__(
                            "<CharCode>%s</CharCode>\s+?<Nominal>(.+?)</Nominal>\s+?<Name>.+?</Name>\s+?<Value>(.+?)</Value>" % (
                            Code), 16)
                        data = comp.search(data)
                        if data:
                            No, Numb = data.groups()
                            answer = "%s/RUB - %s/%s" % (Code, No, Numb)
                        else:
                            answer = self.AnsBase[1]
                else:
                    answer = AnsBase[2]
            else:
                answer = AnsBase[2]
        else:
            Opener = Web("http://www.cbr.ru/scripts/XML_daily.asp")
            try:
                data = Opener.get_page(self.UserAgent)
            except Web.Two.HTTPError as exc:
                answer = str(exc)
            except Exception:
                answer = self.AnsBase[0]
            else:
                data = data.decode("cp1251")
                comp = compile__(
                    "<CharCode>(.+?)</CharCode>\s+?<Nominal>(.+?)</Nominal>\s+?<Name>.+?</Name>\s+?<Value>(.+?)</Value>",
                    16)
                list = comp.findall(data)
                if list:
                    ls, Number = ["\->"], itypes.Number()
                    for Code, No, Numb in sorted(list):
                        ls.append("%d) %s/RUB - %s/%s" % (Number.plus(), Code, No, Numb))
                    if stype == sBase[1]:
                        Answer(AnsBase[11], stype, source, disp)
                    Curls = str.join(chr(10), ls)
                    Message(source[0], Curls, disp)
                else:
                    answer = self.AnsBase[1]
        if locals().has_key(sBase[6]):
            Answer(answer, stype, source, disp)

    def command_jquote(self, stype, source, body, disp):
        if body and isNumber(body):
            Opener = Web("http://jabber-quotes.ru/api/read/?id=%d" % int(body))
        else:
            Opener = Web("http://jabber-quotes.ru/api/read/?id=random")
        try:
            data = Opener.get_page(self.UserAgent)
        except Web.Two.HTTPError as exc:
            answer = str(exc)
        except Exception:
            answer = self.AnsBase[0]
        else:
            data = data.decode("utf-8")
            comp = compile__("<id>(\d+?)</id>\s+?<author>(.+?)</author>\s+?<quote>(.+?)</quote>", 16)
            data = comp.search(data)
            if data:
                Numb, Name, Quote = data.groups()
                lt = chr(10) * 3
                answer = self.decodeHTML("Quote: #%s | by %s\n%s" % (Numb, Name, Quote))
                while (lt in answer):
                    answer = answer.replace(lt, lt[:2])
            else:
                answer = self.AnsBase[1]
        Answer(answer, stype, source, disp)

    def command_ithappens(self, stype, source, body, disp):
        if body and isNumber(body):
            Opener = Web("http://ithappens.ru/story/%d" % int(body))
        else:
            Opener = Web("http://ithappens.ru/random")
        try:
            data = Opener.get_page(self.UserAgent)
        except Web.Two.HTTPError as exc:
            answer = str(exc)
        except Exception:
            answer = self.AnsBase[0]
        else:
            data = data.decode("cp1251")
            data = get_text(data, "<div class=\"text\">", "</p>")
            if data:
                answer = self.decodeHTML(sub_desc(data, {"<p class=\"date\">": chr(32)}))
            else:
                answer = self.AnsBase[1]
        Answer(answer, stype, source, disp)

    def command_gismeteo(self, stype, source, body, disp):
        if body:
            ls = body.split(None, 1)
            Numb = ls.pop(0)
            if ls and isNumber(Numb):
                Numb = int(Numb)
                City = ls.pop(0)
            else:
                Numb = None
                City = body
            if -1 < Numb < 13 or not Numb:
                Opener = Web("http://m.gismeteo.ru/citysearch/by_name/?", [("gis_search", City.encode("utf-8"))])
                try:
                    data = Opener.get_page(self.UserAgent)
                except Web.Two.HTTPError as exc:
                    answer = str(exc)
                except Exception:
                    answer = self.AnsBase[0]
                else:
                    data = data.decode("utf-8")
                    data = get_text(data, "<a href=\"/weather/", "/(1/)*?\">", "\d+")
                    if data:
                        if Numb != None:
                            data = str.join(chr(47), [data, str(Numb) if Numb != 0 else "weekly"])
                        Opener = Web("http://m.gismeteo.ru/weather/%s/" % data)
                        try:
                            data = Opener.get_page(self.UserAgent)
                        except Web.Two.HTTPError as exc:
                            answer = str(exc)
                        except Exception:
                            answer = self.AnsBase[0]
                        else:
                            data = data.decode("utf-8")
                            mark = get_text(data, "<th colspan=\"2\">", "</th>")
                            if Numb != 0:
                                comp = compile__(
                                    '<tr class="tbody">\s+?<th.*?>(.+?)</th>\s+?<td.+?/></td>\s+?</tr>\s+?<tr>\s+?<td.+?>(.+?)</td>\s+?</tr>\s+?<tr class="dl">\s+?<td>&nbsp;</td>\s+?<td class="clpersp"><p>(.*?)</p></td>\s+?</tr>\s+?<tr class="dl"><td class="left">(.+?)</td><td>(.+?)</td></tr>\s+?<tr class="dl"><td class="left">(.+?)</td><td>(.+?)</td></tr>\s+?<tr class="dl bottom"><td class="left">(.+?)</td><td>(.+?)</td></tr>',
                                    16)
                                list = comp.findall(data)
                                if list:
                                    ls = [(self.decodeHTML(mark) if mark else "\->")]
                                    for data in list:
                                        ls.append("{0}:\n\t{2}, {1}\n\t{3} {4}\n\t{5} {6}\n\t{7} {8}".format(*data))
                                    ls.append(self.AnsBase[-2])
                                    answer = self.decodeHTML(str.join(chr(10), ls))
                                else:
                                    answer = self.AnsBase[1]
                            else:
                                comp = compile__(
                                    '<tr class="tbody">\s+?<td class="date" colspan="3"><a.+?>(.+?)</a></td>\s+?</tr>\s+?<tr>\s+?<td rowspan="2"><a.+?/></a></td>\s+?<td class="clpersp"><p>(.*?)</p></td>\s+?</tr>\s+?<tr>\s+?<td.+?>(.+?)</td>',
                                    16)
                                list = comp.findall(data)
                                if list:
                                    ls = [(self.decodeHTML(mark) if mark else "\->")]
                                    for data in list:
                                        ls.append("%s:\n\t%s, %s" % (data))
                                    ls.append(self.AnsBase[-2])
                                    answer = self.decodeHTML(str.join(chr(10), ls))
                                else:
                                    answer = self.AnsBase[1]
                    else:
                        answer = self.AnsBase[5]
            else:
                answer = AnsBase[2]
        else:
            answer = AnsBase[1]
        Answer(answer, stype, source, disp)

    def command_yandex_market(self, stype, source, body, disp):
        if body:
            ls = body.split()
            c1st = (ls.pop(0)).lower()
            if isNumber(c1st):
                if ls:
                    c2nd = ls.pop(0)
                    if isNumber(c2nd):
                        Opener = Web("http://m.market.yandex.ru/spec.xml?hid=%d&modelid=%d" % (int(c1st), int(c2nd)))
                        try:
                            data = Opener.get_page(self.UserAgent_Moz)
                        except Web.Two.HTTPError as exc:
                            answer = str(exc)
                        except Exception:
                            answer = self.AnsBase[0]
                        else:
                            data = data.decode("utf-8", "replace")
                            data = get_text(data, "<h2 class=\"b-subtitle\">", "</div>")
                            if data:
                                answer = self.decodeHTML(sub_desc(data, (
                                chr(10), ("<li>", chr(10)), ("<h2 class=\"b-subtitle\">", chr(10) * 2),
                                ("</h2>", chr(10)))))
                            else:
                                answer = self.AnsBase[5]
                    else:
                        answer = AnsBase[30]
                else:
                    answer = AnsBase[2]
            else:
                body = (body if chr(42) != c1st else body[2:].strip())
                if body:
                    body = body.encode("utf-8")
                    Opener = Web("http://m.market.yandex.ru/search.xml?", [("nopreciser", "1"), ("text", body)])
                    try:
                        data = Opener.get_page(self.UserAgent_Moz)
                    except Web.Two.HTTPError as exc:
                        answer = str(exc)
                    except Exception:
                        answer = self.AnsBase[0]
                    else:
                        data = data.decode("utf-8", "replace")
                        comp = compile__(
                            "<a href=\"http://m\.market\.yandex\.ru/model\.xml\?hid=(\d+?)&amp;modelid=(\d+?)&amp;show-uid=\d+?\">(.+?)</a>",
                            16)
                        list = comp.findall(data)
                        if list:
                            Number = itypes.Number()
                            ls = ["\n[#] [Model Name] (hid & modelid)"]
                            for hid, modelid, name in list:
                                if not name.startswith("<img"):
                                    ls.append("%d) %s (%s %s)" % (Number.plus(), self.sub_ehtmls(name), hid, modelid))
                            answer = str.join(chr(10), ls)
                        else:
                            answer = self.AnsBase[5]
                else:
                    answer = AnsBase[2]
        else:
            answer = AnsBase[1]
        Answer(answer, stype, source, disp)

    commands = (
    (command_jc, "jc", 2,),
    (command_google, "google", 2,),
    (command_google_translate, "tr", 2,),
    (command_imdb, "imdb", 2,),
    (command_python, "python", 2,),
    (command_url_shorten, "shorten", 2,),
    (command_download, "download", 7,),
    (command_paste, "paste", 2,),
    (command_chuck, "chuck", 2,),
    (command_bash, "bash", 2,)
    )

    if DefLANG in ("RU", "UA"):
        commands = commands.__add__((
        (command_kino, "kino", 2,),
        (command_currency, "currency", 2,),
        (command_jquote, "jquote", 2,),
        (command_ithappens, "ithappens", 2,),
        (command_gismeteo, "gismeteo", 2,),
        (command_yandex_market, "market", 2,)
        ))
        CurrencyDesc = CurrencyDesc
    else:
        del kinoHeaders, C3oP, command_kino, command_currency, command_jquote, command_ithappens, command_gismeteo


if DefLANG in ("RU", "UA"):
    del CurrencyDesc
del UserAgents, PasteLangs, LangMap
